"""Pruebas en modo simulación: verifican la cadena sin llaves ni internet.  Ejecutar: pytest -q"""
import json
import os

import pytest

os.environ["MODO_SIMULACION"] = "1"

from mesa import agentes, config, pipeline as pl          # noqa: E402
from mesa import comandos                                  # noqa: E402


@pytest.fixture(autouse=True)
def simulacion(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "MODO_SIMULACION", True)
    monkeypatch.setattr(config, "CARPETA_SALIDAS", str(tmp_path))


def test_formula_posicion_rango_52_semanas():
    ind = agentes.calcular_indicadores({"precio": "250.5", "max_52s": "300", "min_52s": "200", "beta": "0.7"})
    assert ind["posicion_rango_52s_pct"] == 50.5          # (250.5-200)/(300-200)*100
    assert ind["semaforo_beta"].startswith("🟢")


@pytest.mark.parametrize("beta, color", [(0.5, "🟢"), (0.8, "🟡"), (1.2, "🟡"), (1.3, "🔴"), (None, "⚪")])
def test_semaforo_beta(beta, color):
    assert agentes.calcular_indicadores({"beta": beta})["semaforo_beta"].startswith(color)


def test_datos_faltantes_no_rompen_el_calculo():
    ind = agentes.calcular_indicadores({"precio": None, "max_52s": "100", "min_52s": "100"})
    assert ind["posicion_rango_52s_pct"] is None


def test_extraer_json_con_texto_alrededor():
    assert agentes.extraer_json('Aquí tienes: {"a": 1} listo')["a"] == 1
    with pytest.raises(ValueError):
        agentes.extraer_json("sin json")


@pytest.mark.parametrize("entrada, esperado", [(" aapl ", "AAPL"), ("brk.b", "BRK.B")])
def test_ticker_valido(entrada, esperado):
    assert pl.normalizar_ticker(entrada) == esperado


@pytest.mark.parametrize("entrada", ["", "AAPL; rm -rf", "ACCIONMUYLARGAXYZ", "...", "-", "123"])
def test_ticker_invalido(entrada):
    with pytest.raises(ValueError):
        pl.normalizar_ticker(entrada)


def test_cadena_completa_output_es_input():
    avisos = []
    r = pl.pipeline("msft", avisar=avisos.append)
    assert r["entrega_2_analisis"]["ficha"] == r["entrega_1_ficha"]       # 1 → 2
    assert r["entrega_1_ficha"]["ticker"] in r["entrega_3_nota"]          # 2 → 3
    assert agentes.DESCARGO in r["entrega_3_nota"]
    assert any("Entrega 1→2" in a for a in avisos) and any("Entrega 2→3" in a for a in avisos)
    with open(r["archivo"], encoding="utf-8") as f:
        assert json.load(f)["ticker"] == "MSFT"


def test_mcp_caido_usa_respaldo_demo(monkeypatch):
    monkeypatch.setattr(config, "MODO_SIMULACION", False)

    def falla(*args, **kwargs):
        raise ConnectionError("sin red")
    monkeypatch.setattr(agentes, "llamar_claude", falla)
    ficha, herramientas = agentes.agente_recolector("AAPL")
    assert "DEMO" in ficha["fuente"] and herramientas == []


def test_agentes_reales_encadenan_con_claude_simulado(monkeypatch):
    """Imita las respuestas de Claude para revisar el camino 'real' sin gastar llaves."""
    monkeypatch.setattr(config, "MODO_SIMULACION", False)

    def claude_falso(system, mensaje, usar_mcp=False, max_tokens=900):
        if usar_mcp:
            return ('{"nombre":"IBM","sector":"Tech","precio":"250.5","cambio_pct":"-0.8%",'
                    '"pe_ratio":"40.1","beta":"0.7","max_52s":"300","min_52s":"200"}', ["GLOBAL_QUOTE"])
        if "Analista" in system:
            datos = json.loads(mensaje)
            assert datos["indicadores"]["posicion_rango_52s_pct"] == 50.5   # recibió la entrega 1
            return '{"lectura_precio":"a","lectura_riesgo":"b","lectura_valuacion":"c","pregunta_para_investigar":"d"}', []
        assert '"lectura_precio": "a"' in mensaje                           # recibió la entrega 2
        return "IBM: nota sin descargo", []

    monkeypatch.setattr(agentes, "llamar_claude", claude_falso)
    r = pl.pipeline("IBM", avisar=lambda t: None)
    assert r["herramientas_mcp"] == ["GLOBAL_QUOTE"]
    assert r["entrega_1_ficha"]["fuente"] == "Alpha Vantage vía MCP"
    assert r["entrega_3_nota"].endswith(agentes.DESCARGO)                   # el descargo se garantiza


def test_bot_ignora_chats_ajenos_y_responde_ayuda(monkeypatch):
    enviados = []
    monkeypatch.setattr(comandos, "enviar", lambda chat, texto: enviados.append((chat, texto)))
    monkeypatch.setattr(config, "TELEGRAM_CHAT_ID", "111")
    assert comandos.atender({"chat": {"id": 999}, "text": "/analiza AAPL"}) is None
    assert enviados[-1][1] == "Este bot es privado."
    comandos.atender({"chat": {"id": 111}, "text": "hola"})
    assert "Mesa Financiera" in enviados[-1][1]
    r = comandos.atender({"chat": {"id": 111}, "text": "/analiza aapl"})
    assert r["ticker"] == "AAPL" and agentes.DESCARGO in enviados[-1][1]


def test_revision_de_github_actions_atiende_y_confirma(monkeypatch):
    """Simula la corrida de GitHub Actions: 4 mensajes pendientes, límite de 3 por revisión."""
    import revisar_telegram as rt
    pendientes = [{"update_id": i, "message": {"chat": {"id": 111}, "text": t}}
                  for i, t in enumerate(["/analiza AAPL", "hola", "/analiza MSFT", "/analiza NVDA"], start=10)]
    confirmados, enviados = [], []
    monkeypatch.setattr(config, "TELEGRAM_CHAT_ID", "111")
    monkeypatch.setattr(config, "MAX_ANALISIS_POR_RUN", 3)
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "token-de-prueba")
    monkeypatch.setattr(rt, "verificar_bot", lambda: "bot_prueba")
    monkeypatch.setattr(rt, "preparar_polling", lambda: None)
    monkeypatch.setattr(rt, "obtener_mensajes", lambda: pendientes)
    monkeypatch.setattr(rt, "confirmar_leidos", confirmados.append)
    monkeypatch.setattr(comandos, "enviar", lambda chat, texto: enviados.append(texto))
    rt.main()
    assert confirmados == [10, 11, 12]                      # NVDA queda para la siguiente revisión
    assert sum(agentes.DESCARGO in t for t in enviados) == 2  # AAPL y MSFT recibieron su nota


def test_revision_sin_token_termina_sin_error(monkeypatch, capsys):
    """Una copia de la plantilla sin Secrets no debe marcar error en Actions cada 8 minutos."""
    import revisar_telegram as rt
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "")
    rt.main()
    assert "nada que revisar" in capsys.readouterr().out


def test_los_agentes_se_presentan_con_su_nombre():
    """Los nombres del mockup (Batuta, Iris, Euler, Vera) aparecen en Telegram."""
    avisos = []
    r = pl.pipeline("AAPL", avisar=avisos.append)
    texto = "\n".join(avisos)
    for nombre in ("Batuta", "Iris", "Euler", "Vera"):
        assert nombre in texto
    assert r["entrega_3_nota"].startswith(agentes.FIRMA_VERA)


def test_vera_esceptica_dice_lo_que_los_datos_no_dicen():
    """Reto de personalización: Vera ahora es escéptica y directa."""
    assert "escéptica" in agentes.PROMPT_COMUNICADOR
    nota = pl.pipeline("AAPL", avisar=lambda t: None)["entrega_3_nota"]
    assert "Lo que estos datos NO dicen" in nota and "ficticios" in nota       # con datos DEMO
    real = {"ficha": {"fuente": "Alpha Vantage vía MCP"}, "indicadores": {"cambio_pct": -0.8}}
    assert "no es una tendencia" in agentes.lo_que_no_dicen(real)           # con datos reales
    assert nota.endswith(agentes.DESCARGO)                                  # el descargo sigue al final


# ----------------------------------------------------------------------
# Recomendaciones de seguridad aplicadas
# ----------------------------------------------------------------------
def test_iris_sin_herramientas_no_etiqueta_datos_como_reales(monkeypatch):
    """Si Claude responde sin consultar Alpha Vantage, sus cifras no se presentan como reales."""
    monkeypatch.setattr(config, "MODO_SIMULACION", False)
    monkeypatch.setattr(agentes, "llamar_claude", lambda *a, **k: ('{"precio": 999}', []))
    ficha, herramientas = agentes.agente_recolector("AAPL")
    assert "DEMO" in ficha["fuente"] and ficha["precio"] != 999 and herramientas == []


def test_euler_usa_respaldo_si_claude_falla(monkeypatch):
    monkeypatch.setattr(config, "MODO_SIMULACION", False)

    def falla(*a, **k):
        raise ConnectionError("sin red")
    monkeypatch.setattr(agentes, "llamar_claude", falla)
    lectura = agentes.agente_analista({"precio": 150, "max_52s": 180, "min_52s": 120})["lectura"]
    assert {"lectura_precio", "lectura_valuacion", "pregunta_para_investigar"} <= set(lectura)


def test_precio_fuera_de_rango_genera_alerta():
    ind = agentes.calcular_indicadores({"precio": 210, "max_52s": 200, "min_52s": 100})
    assert ind["posicion_rango_52s_pct"] == 110.0 and ind["alerta_datos"]
    assert agentes.calcular_indicadores({"precio": 150, "max_52s": 200, "min_52s": 100})["alerta_datos"] is None


def test_bot_es_privado_aunque_falte_chat_id_en_modo_real(monkeypatch):
    from mesa import telegram_io
    monkeypatch.setattr(config, "TELEGRAM_CHAT_ID", "")
    monkeypatch.setattr(config, "MODO_SIMULACION", False)
    assert telegram_io.chat_autorizado(999) is False


def test_errores_de_red_no_muestran_el_token(monkeypatch):
    import requests
    from mesa import telegram_io
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "123:TOKEN-SECRETO")

    def red_caida(url, **k):
        raise requests.ConnectionError(f"Max retries exceeded with url: {url}")
    monkeypatch.setattr(requests, "get", red_caida)
    with pytest.raises(requests.ConnectionError) as error:
        telegram_io.verificar_bot()
    assert "TOKEN-SECRETO" not in str(error.value) and "***" in str(error.value)


def test_cliente_envia_workspace_si_esta_configurado(monkeypatch):
    """Llaves sin workspace: la API exige el encabezado anthropic-workspace-id."""
    import sys, types
    capturado = {}
    falso = types.SimpleNamespace(Anthropic=lambda **kw: capturado.update(kw) or "cliente")
    monkeypatch.setitem(sys.modules, "anthropic", falso)
    monkeypatch.setattr(agentes, "_cliente", None)
    monkeypatch.setattr(config, "ANTHROPIC_WORKSPACE_ID", "wrkspc_prueba")
    agentes._cliente_claude()
    assert capturado["default_headers"] == {"anthropic-workspace-id": "wrkspc_prueba"}
    monkeypatch.setattr(agentes, "_cliente", None)


def test_vera_usa_respaldo_si_claude_falla(monkeypatch):
    monkeypatch.setattr(config, "MODO_SIMULACION", False)

    def falla(*a, **k):
        raise ConnectionError("sin red")
    monkeypatch.setattr(agentes, "llamar_claude", falla)
    r = pl.pipeline("AAPL", avisar=lambda t: None)
    assert "nota automática" in r["entrega_3_nota"] and r["entrega_3_nota"].endswith(agentes.DESCARGO)


def test_errores_de_agentes_se_registran_sin_llaves(monkeypatch, capsys):
    monkeypatch.setattr(config, "ANTHROPIC_API_KEY", "sk-ant-SECRETA")
    import sys
    monkeypatch.setattr(sys, "stderr", sys.stdout)
    agentes.registrar_error("Iris", ValueError("fallo con llave sk-ant-SECRETA"))
    salida = capsys.readouterr().out
    assert "Iris: ValueError" in salida and "SECRETA" not in salida


def test_iris_sin_cifras_avisa_y_vera_nunca_manda_nota_vacia(monkeypatch):
    """Alpha Vantage respondió sin cifras (límite de consultas) y Claude devolvió texto vacío."""
    monkeypatch.setattr(config, "MODO_SIMULACION", False)

    def claude_falso(system, mensaje, usar_mcp=False, max_tokens=900):
        if usar_mcp:
            return '{"precio": null, "max_52s": null, "min_52s": null}', ["GLOBAL_QUOTE"]
        if "Analista" in system:
            return '{"lectura_precio": "x"}', []
        return "", []                                   # Vera recibe respuesta vacía
    monkeypatch.setattr(agentes, "llamar_claude", claude_falso)
    r = pl.pipeline("MSFT", avisar=lambda t: None)
    assert "límite de consultas" in r["entrega_1_ficha"]["aviso"]
    nota = r["entrega_3_nota"]
    assert "nota automática" in nota and "límite de consultas" in nota and nota.endswith(agentes.DESCARGO)
