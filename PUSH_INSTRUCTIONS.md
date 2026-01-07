# 🚀 Instrucciones para Push Inicial

## ✅ Estado Actual

- ✅ Repositorio GitHub creado: `nekazari-module-intelligence`
- ✅ Carpeta movida a: `/home/g/Documents/nekazari-module-intelligence/`
- ✅ Separada del repo principal (sin conflictos de Git)
- ✅ Estructura completa lista

## 📝 Comandos para Ejecutar

```bash
# 1. Navegar al módulo
cd /home/g/Documents/nekazari-module-intelligence

# 2. Inicializar Git
git init

# 3. Añadir todos los archivos
git add .

# 4. Commit inicial
git commit -m "feat: Initial commit - Intelligence Module v1.0

- Standalone AI/ML module following Nekazari module template
- FastAPI backend with async job processing
- Redis-based job queue
- Orion-LD integration for Prediction entities
- Plugin architecture for ML models
- Kubernetes manifests and CI/CD included"

# 5. Añadir remote (reemplaza con tu URL real si es diferente)
git remote add origin https://github.com/k8-benetis/nekazari-module-intelligence.git

# 6. Push inicial
git branch -M main
git push -u origin main
```

## ✅ Verificación Post-Push

1. **Verifica en GitHub**:
   - Ve a: https://github.com/k8-benetis/nekazari-module-intelligence
   - Deberías ver todos los archivos

2. **Verifica GitHub Actions**:
   - Ve a: https://github.com/k8-benetis/nekazari-module-intelligence/actions
   - El workflow debería ejecutarse automáticamente
   - La imagen Docker se publicará en GHCR

3. **Verifica la imagen Docker**:
   - Ve a: https://github.com/k8-benetis/nekazari-module-intelligence/pkgs/container/intelligence-backend

## 📦 Próximos Pasos

Una vez hecho el push:

1. **Eliminar del repo principal** (si todavía existe):
   ```bash
   cd /home/g/Documents/nekazari-public
   # Si todavía existe services/intelligence-service/, eliminarlo
   git rm -r services/intelligence-service/  # Si estaba trackeado
   git commit -m "chore: Remove intelligence-service (now external module)"
   git push
   ```

2. **Desplegar en Kubernetes** (cuando esté listo):
   ```bash
   # En el servidor de producción
   kubectl apply -f k8s/backend-deployment.yaml
   ```

3. **Registrar el módulo**:
   ```bash
   kubectl exec -it <postgres-pod> -n nekazari -- \
     psql -U nekazari -d nekazari -f /path/to/k8s/registration.sql
   ```

## ⚠️ Notas Importantes

- El módulo está **completamente separado** del repo principal
- No hay dependencias de código entre repos
- Cada módulo tiene su propio CI/CD
- Las imágenes se publican en GHCR automáticamente

