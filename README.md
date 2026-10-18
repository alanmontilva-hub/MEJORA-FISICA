# Camino a 74

App de Android para seguir tu rutina de ejercicio, tus comidas, tu diario y tu progreso de peso (de 80 a 74 kg).
Funciona sin internet, guarda todo en el teléfono y tiene asistente de voz y recordatorios.

## Instalar en el teléfono

1. Abre en el teléfono: https://github.com/alanmontilva-hub/MEJORA-FISICA/releases/latest
2. Descarga `camino-a-74.apk`.
3. Ábrelo. Si Android lo pide, permite "instalar apps desconocidas" para el navegador o el gestor de archivos que usaste.
4. Abre la app y dale permiso de micrófono y de notificaciones cuando lo pida.

Cada vez que se actualiza el código (rama `main`), GitHub compila un APK nuevo y lo deja en esa misma página.
Se instala encima del anterior sin perder tus datos porque siempre se firma con la misma llave (`signing/debug.keystore`).

## Cómo está hecho

- `www/`: la app (HTML, CSS y JavaScript sin dependencias).
- `capacitor.config.json`: configuración de Capacitor, que convierte `www/` en app de Android.
- `.github/workflows/android.yml`: compila el APK en GitHub Actions.
- `scripts/prepare_android.py`: permisos de micrófono y notificaciones, y número de versión.
- `assets/`: ícono de la app.

## Datos

- Todo se guarda en el teléfono. En Progreso, "Respaldo" copia tus datos para guardarlos fuera de la app.
- La clave de la API de Anthropic (opcional) se guarda solo en el teléfono y no entra en el respaldo.

## Fuentes de los números

- Meta de proteína: metaanálisis en Clinical Nutrition ESPEN, 2024 (https://pubmed.ncbi.nlm.nih.gov/39002131/).
- Calorías de la cuerda: 11,0 METs del Compendio de Actividad Física (https://pacompendium.com/conditioning-exercise/).
