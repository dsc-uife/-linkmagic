# LinkMagic

Herramienta CLI para gestionar links desde terminal. Acorta, genera QR, previsualiza, convierte links de Amazon en afiliados, añade UTMs y verifica links rotos. Todo en un comando.

## Instalacion

git clone https://github.com/dsc-uife/-linkmagic.git
cd linkmagic
pip install requests beautifulsoup4

## Uso

python linkmagic.py [comando] [opciones]

## Comandos Gratis

acortar [url] - Acorta un link
qr [url] - Genera QR del link

## Comandos PRO

preview [url] - Vista previa (titulo + descripcion)
afiliado [url] - Link Amazon a afiliado + acortado
utm [url] --source X --campaign Y - Link con UTMs + acortado
check [url] - Verifica si un link esta vivo/roto

## Obten LinkMagic PRO

17 euros, pago unico, actualizaciones de por vida:

https://dsc2026.gumroad.com/l/anjmyy

## Ejemplos

python linkmagic.py acortar https://ejemplo.com/muy-largo
python linkmagic.py qr https://ejemplo.com
python linkmagic.py afiliado https://www.amazon.es/dp/B08N5WRWNW
python linkmagic.py utm https://ejemplo.com --source twitter --campaign promo
python linkmagic.py check https://ejemplo.com

## Licencia

MIT. El codigo es libre. Las funciones PRO requieren licencia.
