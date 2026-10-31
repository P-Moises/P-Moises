# Opciones de portada

Cada archivo es una versión completa de la portada (`README.md`). Ninguna está activada todavía.

| Opción | En una línea |
|---|---|
| [1-actual](1-actual.md) | La portada de hoy, guardada tal cual: colorida, con emojis y tono informal. |
| [2-estudio](2-estudio.md) | Fondo casi negro con acento lima: el nombre grande, una línea que se escribe sola y órbitas lentas de «Multiverso». |
| [3-editorial](3-editorial.md) | Estilo revista en papel crema y terracota: letra con serifa, subrayados que se dibujan y un sello que gira. |
| [4-plano](4-plano.md) | Plano técnico azul con detalles ámbar: cuadrícula, línea de escaneo, cotas que se dibujan y una ficha tipo cajetín. |

## Qué se mueve

Las animaciones están dentro de los SVG de `recursos/` y GitHub las muestra solas (no usan JavaScript).

- **Línea que se escribe sola** (opciones 2 y 4): el mismo efecto de máquina de escribir de la portada actual.
- **Proceso de 5 pasos**: en cada opción un dibujo distinto recorre «entender, estudiar la competencia,
  diseñar, construir y probar en un celular real».
- Si el visitante tiene activado «reducir movimiento» en su equipo, los dibujos se quedan quietos y se leen igual.

## Cómo activar una opción

1. Copia el contenido de la opción elegida (por ejemplo `2-estudio.md`) dentro de `README.md`.
2. Deja la carpeta `opciones/recursos/` donde está: las imágenes se cargan desde ahí.
3. Rellena el contacto marcado como **FALTA** (correo o LinkedIn).

## Cambiar los dibujos

Los SVG se fabrican con `recursos/generar_svg.py` (colores, textos y tiempos están arriba de cada bloque):

```
python opciones/recursos/generar_svg.py opciones/recursos
```

Reglas de diseño usadas: guía del Multiverso y habilidades de Emil Kowalski (licencia MIT).
