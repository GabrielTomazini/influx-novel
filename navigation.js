// Script para prevenir cliques múltiplos nos botões de navegação
(function() {
    'use strict';
    
    // Prevenir múltiplos cliques nos links de navegação
    function preventMultipleClicks() {
        const navigationLinks = document.querySelectorAll('.navigation a');
        let navigationClicked = false;
        
        navigationLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Se já houve um clique, prevenir novos cliques
                if (navigationClicked) {
                    e.preventDefault();
                    return false;
                }
                
                // Marcar que houve um clique
                navigationClicked = true;
                
                // Desabilitar visualmente todos os links de navegação
                navigationLinks.forEach(navLink => {
                    navLink.classList.add('disabled');
                });
                
                // Armazenar no sessionStorage para evitar cliques mesmo após o carregamento
                sessionStorage.setItem('navigating', 'true');
                
                // Permitir que o link funcione normalmente
                return true;
            });
        });
        
        // Limpar o estado quando a página carregar
        window.addEventListener('pageshow', function() {
            sessionStorage.removeItem('navigating');
        });
        
        // Verificar se estava navegando ao carregar a página
        if (sessionStorage.getItem('navigating') === 'true') {
            const navigationLinks = document.querySelectorAll('.navigation a');
            navigationLinks.forEach(link => {
                link.classList.add('disabled');
            });
            
            // Remover o estado após 2 segundos (tempo de segurança)
            setTimeout(() => {
                sessionStorage.removeItem('navigating');
                navigationLinks.forEach(link => {
                    link.classList.remove('disabled');
                });
            }, 2000);
        }
    }
    
    // Executar quando o DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', preventMultipleClicks);
    } else {
        preventMultipleClicks();
    }
})();
