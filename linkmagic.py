import sys
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, parse_qs

# ========== FUNCIONES GRATIS ==========

def acortar(url):
    """Acorta un link usando TinyURL"""
    respuesta = requests.get(f"https://tinyurl.com/api-create.php?url={url}")
    return respuesta.text

def qr(url):
    """Genera link de QR"""
    return f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url}"

# ========== FUNCIONES PRO ==========

def preview(url):
    """PRO: Extrae título y descripción de cualquier web"""
    if not verificar_licencia():
        mostrar_mensaje_pro("preview")
        return None
    
    try:
        respuesta = requests.get(url, timeout=10, 
                                headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        titulo = soup.title.string.strip() if soup.title else "Sin título"
        descripcion = soup.find('meta', attrs={'name': 'description'})
        descripcion = descripcion['content'].strip() if descripcion else "Sin descripción"
        
        return f"""
        📄 Título: {titulo}
        📝 Descripción: {descripcion[:150]}...
        """
    except:
        return "❌ No se pudo acceder al link"

def afiliado(url, tag=None):
    """PRO: Convierte link de Amazon en link de afiliado y lo acorta"""
    if not verificar_licencia():
        mostrar_mensaje_pro("afiliado")
        return None
    
    if not tag:
        tag = cargar_tag()
    
    if not tag:
        print("⚠️  No hay tag de afiliado configurado. Usa:")
        print("   python linkmagic.py config --tag TU-TAG-21")
        return None
    
    dominios_amazon = ['amazon.com', 'amazon.es', 'amazon.co.uk', 'amazon.de', 
                       'amazon.fr', 'amazon.it', 'amazon.com.mx', 'amazon.com.br']
    
    es_amazon = False
    for dominio in dominios_amazon:
        if dominio in url:
            es_amazon = True
            break
    
    if not es_amazon:
        return "❌ El link no parece ser de Amazon"
    
    url_base = url.split('?')[0]
    
    if '?' in url:
        url_afiliado = f"{url}&tag={tag}"
    else:
        url_afiliado = f"{url}?tag={tag}"
    
    link_corto = acortar(url_afiliado)
    
    return f"""
    🔗 Link original: {url}
    💰 Link afiliado: {url_afiliado}
    ✂️ Link acortado: {link_corto}
    
    ✅ ¡Listo para publicar y ganar comisiones!
    """

def utm(url, source=None, medium=None, campaign=None, term=None, content=None):
    """PRO: Añade parámetros UTM a un link y lo acorta"""
    if not verificar_licencia():
        mostrar_mensaje_pro("utm")
        return None
    
    if not source:
        print("⚠️  UTM source es obligatorio. Usa:")
        print("   python linkmagic.py utm [url] --source twitter --campaign promo")
        return None
    
    # Construir parámetros UTM
    params = []
    params.append(f"utm_source={source}")
    if medium: params.append(f"utm_medium={medium}")
    if campaign: params.append(f"utm_campaign={campaign}")
    if term: params.append(f"utm_term={term}")
    if content: params.append(f"utm_content={content}")
    
    # Añadir a la URL
    if '?' in url:
        url_utm = f"{url}&{'&'.join(params)}"
    else:
        url_utm = f"{url}?{'&'.join(params)}"
    
    link_corto = acortar(url_utm)
    
    return f"""
    🔗 Link original: {url}
    📊 Link con UTM: {url_utm}
    ✂️ Link acortado: {link_corto}
    
    ✅ ¡Listo para trackear tu campaña!
    """

def check(url):
    """PRO: Verifica si un link está vivo o roto"""
    if not verificar_licencia():
        mostrar_mensaje_pro("check")
        return None
    
    try:
        respuesta = requests.get(url, timeout=10, 
                                headers={'User-Agent': 'Mozilla/5.0'})
        
        if respuesta.status_code == 200:
            return f"""
    ✅ Link VIVO
    🔗 URL: {url}
    📡 Código: {respuesta.status_code}
    ⚡ Tiempo: {respuesta.elapsed.total_seconds():.2f}s
            """
        elif respuesta.status_code in [301, 302]:
            redirect = respuesta.headers.get('Location', 'desconocido')
            return f"""
    🔀 Link REDIRIGE
    🔗 URL: {url}
    📡 Código: {respuesta.status_code}
    ➡️ Redirige a: {redirect}
            """
        else:
            return f"""
    ⚠️ Link PROBLEMÁTICO
    🔗 URL: {url}
    📡 Código: {respuesta.status_code}
            """
    except requests.exceptions.Timeout:
        return f"⏰ Tiempo agotado: {url} no responde"
    except:
        return f"❌ Link ROTO o inaccesible: {url}"

def configurar_tag(tag):
    """PRO: Guarda el tag de afiliado de Amazon"""
    if not verificar_licencia():
        mostrar_mensaje_pro("config")
        return None
    
    with open("tag_afiliado.txt", "w") as f:
        f.write(tag.strip())
    return f"✅ Tag de afiliado guardado: {tag.strip()}"

def cargar_tag():
    """Carga el tag de afiliado guardado"""
    try:
        with open("tag_afiliado.txt", "r") as f:
            return f.read().strip()
    except:
        return None

# ========== SISTEMA DE LICENCIA ==========

def verificar_licencia():
    return os.path.exists("licencia.key")

def mostrar_mensaje_pro(comando):
    print(f"""
╔══════════════════════════════════════════════╗
║  🔒 '{comando}' es función PRO              ║
║                                              ║
║  Consigue LinkMagic PRO por solo 27€:        ║
║  https://gumroad.com/l/linkmagic-pro         ║
║                                              ║
║  Incluye:                                    ║
║  • preview  - Vista previa de links          ║
║  • afiliado - Amazon afiliado automático     ║
║  • utm      - Generador de campañas UTM      ║
║  • check    - Detector de links rotos/vivos  ║
║  • config   - Guardar tag de afiliado        ║
║  • Actualizaciones de por vida               ║
╚══════════════════════════════════════════════╝
    """)

# ========== PROGRAMA PRINCIPAL ==========

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════╗
║          LinkMagic - CLI Link Tool           ║
╚══════════════════════════════════════════════╝

Uso: python linkmagic.py [comando] [opciones]

Comandos GRATIS:
  acortar [url]                    Acorta un link
  qr [url]                         Genera QR del link

Comandos PRO:
  preview [url]                    Vista previa (título + descripción)
  afiliado [url]                   Link Amazon afiliado + acortado
  utm [url] --source [fuente]      Link con UTMs + acortado
  check [url]                      Verifica si un link está vivo
  config --tag [TU-TAG]            Guarda tag de afiliado

Ejemplos:
  python linkmagic.py acortar https://ejemplo.com/muy-largo
  python linkmagic.py qr https://ejemplo.com
  python linkmagic.py preview https://ejemplo.com
  python linkmagic.py afiliado https://www.amazon.es/dp/B08N5WRWNW
  python linkmagic.py utm https://ejemplo.com --source twitter --campaign promo
  python linkmagic.py check https://ejemplo.com
  python linkmagic.py config --tag mipagina-21
        """)
    
    elif sys.argv[1] == "config" and len(sys.argv) > 2 and sys.argv[2] == "--tag":
        tag = sys.argv[3] if len(sys.argv) > 3 else None
        if tag:
            resultado = configurar_tag(tag)
            if resultado:
                print(resultado)
    
    elif sys.argv[1] == "utm":
        if len(sys.argv) < 3:
            print("❌ Uso: python linkmagic.py utm [url] --source [fuente]")
        else:
            url = sys.argv[2]
            source = None; medium = None; campaign = None; term = None; content = None
            
            args = sys.argv[3:]
            for i, arg in enumerate(args):
                if arg == "--source" and i+1 < len(args): source = args[i+1]
                elif arg == "--medium" and i+1 < len(args): medium = args[i+1]
                elif arg == "--campaign" and i+1 < len(args): campaign = args[i+1]
                elif arg == "--term" and i+1 < len(args): term = args[i+1]
                elif arg == "--content" and i+1 < len(args): content = args[i+1]
            
            resultado = utm(url, source, medium, campaign, term, content)
            if resultado:
                print(resultado)
    
    else:
        comando = sys.argv[1]
        url = sys.argv[2] if len(sys.argv) > 2 else None
        
        if comando == "acortar" and url:
            print(f"✅ Link acortado: {acortar(url)}")
        elif comando == "qr" and url:
            print(f"✅ QR generado: {qr(url)}")
        elif comando == "preview" and url:
            resultado = preview(url)
            if resultado:
                print(resultado)
        elif comando == "afiliado" and url:
            resultado = afiliado(url)
            if resultado:
                print(resultado)
        elif comando == "check" and url:
            resultado = check(url)
            if resultado:
                print(resultado)
        else:
            print(f"❌ Comando '{comando}' no reconocido o falta URL")