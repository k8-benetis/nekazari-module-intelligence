# Quick Start Guide - Intelligence Module

## ✅ Completado

El módulo está completamente reorganizado siguiendo el patrón del `module-template`. Estructura lista para crear el repositorio GitHub.

## 📋 Pasos Finales (Acción Requerida)

### ✅ Ubicación Correcta

El módulo está ahora en:
```
/home/g/Documents/nekazari-module-intelligence/
```

**Importante**: Ya está fuera del repo principal (`nekazari-public/`), siguiendo el patrón de otros módulos como `nekazari-module-template` y `nekazari-module-vegetation-health`.

### 1. Crear Repositorio en GitHub

```bash
# Ve a GitHub y crea:
# https://github.com/k8-benetis/nekazari-module-intelligence

# NO inicialices con README, .gitignore, o licencia (ya los tenemos)
```

### 2. Inicializar Git y Hacer Push

```bash
cd /home/g/Documents/nekazari-module-intelligence

# Inicializar repositorio
git init
git add .
git commit -m "feat: Initial commit - Intelligence Module v1.0

- Standalone AI/ML module following Nekazari module template
- FastAPI backend with async job processing
- Redis-based job queue
- Orion-LD integration for Prediction entities
- Plugin architecture for ML models
- Kubernetes manifests and CI/CD included"

# Conectar con GitHub
git remote add origin https://github.com/k8-benetis/nekazari-module-intelligence.git

# Push inicial
git branch -M main
git push -u origin main
```

### 3. Verificar CI/CD

Después del push, verifica que el workflow de GitHub Actions se ejecute correctamente:
- Ve a: `https://github.com/k8-benetis/nekazari-module-intelligence/actions`
- Debería aparecer un workflow ejecutándose

### 4. (Opcional) Crear Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

Esto creará una imagen Docker con tag `v1.0.0`.

## 📦 Estructura Final

```
module-intelligence/
├── backend/
│   ├── app/
│   │   ├── main.py              ✅ FastAPI app factory
│   │   ├── config.py            ✅ Config con pydantic-settings
│   │   ├── api/__init__.py      ✅ Todos los endpoints
│   │   ├── core/                ✅ Jobs, worker, orion, redis
│   │   ├── plugins/             ✅ Plugin system
│   │   └── middleware/          ✅ (Opcional para futuro)
│   ├── tests/                   ✅ Test básico
│   ├── Dockerfile               ✅ Multi-stage build
│   └── requirements.txt         ✅ Dependencias + ML placeholders
├── k8s/
│   ├── backend-deployment.yaml  ✅ Deployment K8s
│   └── registration.sql         ✅ SQL para registro
├── .github/workflows/
│   └── build-push.yml           ✅ CI/CD
├── manifest.json                ✅ Metadata del módulo
├── env.example                  ✅ Template de variables
├── README.md                    ✅ Documentación completa
├── SETUP.md                     ✅ Guía de setup
└── MIGRATION.md                 ✅ Guía de migración
```

## 🔧 Próximos Pasos Después del Push

1. **Actualizar Core Repository**:
   - Eliminar `services/intelligence-service/` del repo principal
   - Actualizar documentación si es necesario

2. **Desplegar en Kubernetes**:
   ```bash
   kubectl apply -f k8s/backend-deployment.yaml
   kubectl exec -it <postgres-pod> -n nekazari -- psql -U nekazari -d nekazari -f k8s/registration.sql
   ```

3. **Configurar Ingress** (si es necesario):
   - Añadir ruta en el Ingress principal para `/api/intelligence/*`

## ✅ Checklist Pre-Push

- [x] Estructura sigue el patrón del module-template
- [x] Imports corregidos (app.* en lugar de intelligence_service.*)
- [x] Dockerfile multi-stage optimizado
- [x] CI/CD workflow configurado
- [x] Manifests K8s listos
- [x] manifest.json creado
- [x] Documentación completa
- [ ] Repositorio GitHub creado (ACCION REQUERIDA)
- [ ] Git init y push (ACCION REQUERIDA)

## 🎯 Notas Importantes

- **No hay frontend**: Este módulo es solo backend (API REST)
- **Comunicación**: Solo vía REST API y Orion-LD (Prediction entities)
- **Sin dependencias del Core**: Completamente independiente
- **Listo para ML**: Descomenta librerías en `requirements.txt` cuando las necesites


