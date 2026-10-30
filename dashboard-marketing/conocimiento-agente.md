# Base de conocimiento: Tablero "Desempeño de campañas de marketing"

Este documento describe por completo el tablero interactivo publicado en https://montserratsanchez.github.io/MESA-FINANCIERA/dashboard-marketing/ . Todas las cifras de este documento son exactamente las que muestra el tablero.

## 1. Qué es el tablero
- Es un dashboard interactivo en HTML para hacer un análisis exploratorio básico del desempeño de campañas de marketing.
- **Los datos son sintéticos (inventados para el ejemplo).** No son resultados reales de ninguna empresa. Se generan con una semilla fija, así que siempre salen iguales.
- Periodo: de noviembre 2025 a octubre 2026 (12 meses).
- Moneda: pesos mexicanos (MXN).
- Tamaño: 240 registros = 12 meses × 5 canales × 4 regiones.
- Canales: Email, Redes sociales, SEO, Pago por clic, Influencers.
- Regiones: CDMX, Monterrey, Guadalajara, Puebla.
- Campos de cada registro: mes, canal, región, inversión, impresiones, clics, conversiones e ingresos.

## 2. Cómo se usa el tablero
- **Filtros** en la parte superior: canal, región, mes inicial ("Desde") y mes final ("Hasta"). El botón "Restablecer" quita todos los filtros.
- **Clic en una barra** de la gráfica "ROAS por canal" filtra ese canal; otro clic quita el filtro.
- **KPIs**: seis tarjetas (inversión, ingresos, conversiones, ROAS, costo por conversión y CTR). Cada una se compara con el periodo anterior de la misma duración, si existe dentro de los datos. Con el periodo completo aparece "Sin periodo anterior comparable".
- **Gráficas**: línea de ingresos vs. inversión por mes; barras de ROAS por canal con una línea punteada en 1.0 (punto de equilibrio); mapa de calor de conversiones por región y canal; dispersión de inversión vs. ingresos por registro.
- **Lectura automática**: un panel que resume el filtro actual y etiqueta cada frase como Dato, Inferencia o Supuesto.
- **Tabla "Resumen por canal"**: se ordena al hacer clic en cada encabezado.
- **Botón "Descargar CSV filtrado"**: descarga los registros que cumplen el filtro actual.
- También incluye un muro de Padlet llamado "Conceptos clave de marketing" y este asistente de voz.

## 3. Definiciones de las métricas
- **Inversión**: dinero gastado en publicidad en el canal.
- **Impresiones**: veces que se mostró el anuncio o contenido.
- **Clics**: veces que alguien hizo clic.
- **Conversiones**: ventas o acciones objetivo logradas.
- **Ingresos**: dinero generado por las conversiones.
- **ROAS** (retorno sobre la inversión publicitaria) = ingresos ÷ inversión. Un ROAS de 3x significa que por cada peso invertido regresaron 3 pesos. Si es menor a 1x no se recupera la inversión.
- **Costo por conversión (CPA)** = inversión ÷ conversiones.
- **CTR** (tasa de clics) = clics ÷ impresiones.
- **Tasa de conversión** = conversiones ÷ clics.

## 4. Totales del periodo completo (noviembre 2025 a octubre 2026, todos los canales y regiones)
- Inversión total: $6,024,986 MXN
- Ingresos totales: $17,620,222 MXN
- Conversiones totales: 21,131
- Impresiones: 35,406,690
- Clics: 703,367
- ROAS total: 2.92x
- Costo por conversión: $285 MXN
- CTR: 1.99%
- Tasa de conversión: 3.00%

## 5. Resultados por canal (periodo completo, ordenados de mayor a menor ROAS)
| Canal | Inversión | Ingresos | Conversiones | ROAS | Costo por conversión | CTR | Tasa de conversión |
|---|---|---|---|---|---|---|---|
| Email | $536,143 MXN | $2,625,398 MXN | 2,687 | 4.90x | $200 MXN | 2.02% | 3.03% |
| SEO | $789,004 MXN | $3,589,751 MXN | 4,418 | 4.55x | $179 MXN | 2.48% | 2.09% |
| Pago por clic | $1,949,751 MXN | $6,717,716 MXN | 7,376 | 3.45x | $264 MXN | 3.05% | 3.10% |
| Redes sociales | $1,513,436 MXN | $3,298,484 MXN | 4,753 | 2.18x | $318 MXN | 1.20% | 4.63% |
| Influencers | $1,236,652 MXN | $1,388,873 MXN | 1,897 | 1.12x | $652 MXN | 1.02% | 3.04% |
- Email ocupa el lugar 1 de 5 en ROAS con 4.90x: invirtió $536,143 MXN, generó $2,625,398 MXN y logró 2,687 conversiones.
- SEO ocupa el lugar 2 de 5 en ROAS con 4.55x: invirtió $789,004 MXN, generó $3,589,751 MXN y logró 4,418 conversiones.
- Pago por clic ocupa el lugar 3 de 5 en ROAS con 3.45x: invirtió $1,949,751 MXN, generó $6,717,716 MXN y logró 7,376 conversiones.
- Redes sociales ocupa el lugar 4 de 5 en ROAS con 2.18x: invirtió $1,513,436 MXN, generó $3,298,484 MXN y logró 4,753 conversiones.
- Influencers ocupa el lugar 5 de 5 en ROAS con 1.12x: invirtió $1,236,652 MXN, generó $1,388,873 MXN y logró 1,897 conversiones.

## 6. Resultados por región (periodo completo, ordenadas por ingresos)
| Región | Inversión | Ingresos | Conversiones | ROAS | Costo por conversión |
|---|---|---|---|---|---|
| CDMX | $1,975,730 MXN | $5,679,790 MXN | 6,743 | 2.87x | $293 MXN |
| Monterrey | $1,566,959 MXN | $4,632,593 MXN | 5,580 | 2.96x | $281 MXN |
| Guadalajara | $1,421,017 MXN | $4,162,960 MXN | 5,023 | 2.93x | $283 MXN |
| Puebla | $1,061,280 MXN | $3,144,879 MXN | 3,785 | 2.96x | $280 MXN |

## 7. Resultados por mes (todos los canales y regiones)
| Mes | Inversión | Ingresos | Conversiones | ROAS |
|---|---|---|---|---|
| noviembre 2025 | $515,962 MXN | $1,564,536 MXN | 1,988 | 3.03x |
| diciembre 2025 | $489,905 MXN | $1,690,673 MXN | 2,118 | 3.45x |
| enero 2026 | $520,750 MXN | $1,308,678 MXN | 1,513 | 2.51x |
| febrero 2026 | $501,054 MXN | $1,300,941 MXN | 1,601 | 2.60x |
| marzo 2026 | $480,740 MXN | $1,326,848 MXN | 1,620 | 2.76x |
| abril 2026 | $495,730 MXN | $1,591,806 MXN | 1,743 | 3.21x |
| mayo 2026 | $482,099 MXN | $1,528,209 MXN | 1,787 | 3.17x |
| junio 2026 | $543,613 MXN | $1,489,634 MXN | 1,840 | 2.74x |
| julio 2026 | $489,418 MXN | $1,430,753 MXN | 1,676 | 2.92x |
| agosto 2026 | $500,158 MXN | $1,479,656 MXN | 1,715 | 2.96x |
| septiembre 2026 | $491,425 MXN | $1,377,533 MXN | 1,643 | 2.80x |
| octubre 2026 | $514,132 MXN | $1,530,955 MXN | 1,887 | 2.98x |

## 8. Conversiones por región y canal (lo que muestra el mapa de calor)
| Región | Email | Redes sociales | SEO | Pago por clic | Influencers |
|---|---|---|---|---|---|
| CDMX | 837 | 1,473 | 1,308 | 2,512 | 613 |
| Monterrey | 687 | 1,297 | 1,137 | 1,961 | 498 |
| Guadalajara | 682 | 1,117 | 1,169 | 1,569 | 486 |
| Puebla | 481 | 866 | 804 | 1,334 | 300 |

## 9. ROAS por región y canal
| Región | Email | Redes sociales | SEO | Pago por clic | Influencers |
|---|---|---|---|---|---|
| CDMX | 4.96x | 2.10x | 4.08x | 3.56x | 1.15x |
| Monterrey | 5.12x | 2.28x | 4.70x | 3.27x | 1.13x |
| Guadalajara | 4.75x | 2.10x | 5.12x | 3.36x | 1.15x |
| Puebla | 4.69x | 2.28x | 4.41x | 3.63x | 1.01x |

## 10. Ingresos por mes y canal
| Mes | Email | Redes sociales | SEO | Pago por clic | Influencers |
|---|---|---|---|---|---|
| noviembre 2025 | $189,541 MXN | $267,425 MXN | $364,221 MXN | $602,606 MXN | $140,743 MXN |
| diciembre 2025 | $288,770 MXN | $346,410 MXN | $357,458 MXN | $543,121 MXN | $154,914 MXN |
| enero 2026 | $145,761 MXN | $256,493 MXN | $289,549 MXN | $511,051 MXN | $105,824 MXN |
| febrero 2026 | $198,923 MXN | $266,881 MXN | $218,881 MXN | $530,969 MXN | $85,287 MXN |
| marzo 2026 | $178,082 MXN | $293,326 MXN | $287,272 MXN | $470,474 MXN | $97,694 MXN |
| abril 2026 | $302,603 MXN | $253,994 MXN | $357,240 MXN | $568,978 MXN | $108,991 MXN |
| mayo 2026 | $200,495 MXN | $254,177 MXN | $366,085 MXN | $628,349 MXN | $79,103 MXN |
| junio 2026 | $218,172 MXN | $263,313 MXN | $260,647 MXN | $648,227 MXN | $99,275 MXN |
| julio 2026 | $206,775 MXN | $261,385 MXN | $327,665 MXN | $492,576 MXN | $142,352 MXN |
| agosto 2026 | $226,014 MXN | $242,873 MXN | $238,454 MXN | $665,713 MXN | $106,602 MXN |
| septiembre 2026 | $246,791 MXN | $280,262 MXN | $237,197 MXN | $473,071 MXN | $140,212 MXN |
| octubre 2026 | $223,471 MXN | $311,945 MXN | $285,082 MXN | $582,581 MXN | $127,876 MXN |

## 11. Hallazgos principales (cada uno marcado como Dato, Inferencia o Supuesto)
1. **Dato:** Email tiene el ROAS más alto (4.90x) y Influencers el más bajo (1.12x).
2. **Dato:** SEO tiene el menor costo por conversión ($179 MXN) y Influencers el mayor ($652 MXN).
3. **Dato:** Pago por clic es el canal con más conversiones (7,376), aunque no es el de mejor ROAS.
4. **Dato:** Influencers apenas supera el punto de equilibrio (ROAS 1.12x): por cada peso invertido recupera muy poco más de un peso.
5. **Dato:** CDMX es la región con más ingresos ($5,679,790 MXN) y Puebla la de menos ($3,144,879 MXN).
6. **Dato:** el mes con más ingresos es diciembre 2025 ($1,690,673 MXN) y el de menos es febrero 2026 ($1,300,941 MXN).
7. **Dato:** en el primer semestre (nov 2025 a abr 2026) el ROAS fue 2.92x y en el segundo (may a oct 2026) fue 2.93x.
8. **Inferencia:** reasignar parte del presupuesto de Influencers hacia Email o SEO podría mejorar el ROAS total, siempre que esos canales mantengan su rendimiento al recibir más dinero. Esto no se puede comprobar con estos datos.
9. **Inferencia:** las diferencias entre canales son correlaciones; los datos no prueban que el canal sea la causa del resultado.
10. **Supuesto:** el pico de diciembre se programó a propósito en los datos sintéticos como efecto de temporada navideña; no es una observación real.

## 12. Límites del tablero (lo que NO se puede afirmar)
- Los datos son sintéticos: no sirven para tomar decisiones reales de negocio.
- No hay datos de costos de producto, utilidad, clientes individuales ni atribución multicanal.
- No hay datos antes de noviembre 2025 ni después de octubre 2026.
- No se puede saber por qué un canal rinde más; solo que rinde más en estos datos.
