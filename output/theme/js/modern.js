// Modern interactivity enhancements for WEBfolio

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavigation();
    initScrollEffects();
    initSearch();
    initProjectCards();
    initBackToTop();
    initScrollProgress();
    initPageEnhancements();
    initPerformanceOptimizations();
    
    // Additional masonry initialization after complete page load
    window.addEventListener('load', () => {
        setTimeout(() => {
            initMasonryLayout();
        }, 200);
    });
    
    console.log('WEBfolio modern theme loaded successfully!');
});

// Navigation functionality
function initNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            navToggle.setAttribute('aria-expanded', 
                navToggle.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
            );
        });

        // Close mobile menu when clicking on a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
}

// Scroll effects
function initScrollEffects() {
    // Header hide/show on scroll
    let lastScrollTop = 0;
    const header = document.querySelector('header');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });

    // Parallax effect for hero section
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.3;
            hero.style.transform = `translateY(${parallax}px)`;
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Search functionality
function initSearch() {
    const searchInput = document.querySelector('#search');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const query = this.value.toLowerCase().trim();
                const cards = document.querySelectorAll('.project-card');
                
                cards.forEach(card => {
                    const title = card.querySelector('.project-title')?.textContent.toLowerCase() || '';
                    const summary = card.querySelector('.project-summary')?.textContent.toLowerCase() || '';
                    const tags = Array.from(card.querySelectorAll('.tag')).map(tag => tag.textContent.toLowerCase()).join(' ');
                    
                    const isMatch = !query || title.includes(query) || summary.includes(query) || tags.includes(query);
                    
                    card.style.display = isMatch ? 'block' : 'none';
                    card.style.opacity = isMatch ? '1' : '0';
                    card.style.transform = isMatch ? 'translateY(0)' : 'translateY(20px)';
                });

                // Show "no results" message if needed
                const visibleCards = Array.from(cards).filter(card => card.style.display !== 'none');
                showNoResultsMessage(visibleCards.length === 0 && query);
                
                // Пересчитать masonry layout после фильтрации
                setTimeout(() => {
                    initMasonryLayout();
                }, 100);
            }, 300);
        });
    }
}

function showNoResultsMessage(show) {
    let noResultsMsg = document.querySelector('.no-results-message');
    
    if (show && !noResultsMsg) {
        noResultsMsg = document.createElement('div');
        noResultsMsg.className = 'no-results-message text-center';
        noResultsMsg.innerHTML = `
            <p style="color: var(--text-light); margin: var(--spacing-xl) 0;">
                📝 Проекты по вашему запросу не найдены
            </p>
        `;
        const projectsGrid = document.querySelector('.projects-grid');
        if (projectsGrid) {
            projectsGrid.parentNode.insertBefore(noResultsMsg, projectsGrid.nextSibling);
        }
    } else if (!show && noResultsMsg) {
        noResultsMsg.remove();
    }
}

// Project cards animations and masonry layout
function initProjectCards() {
    const projectCards = document.querySelectorAll('.project-card');
    
    // Add staggered animation
    projectCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });

    // Initialize masonry layout
    initMasonryLayout();

    // Intersection Observer for scroll animations
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        projectCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
    }
}

// Back to top button
function initBackToTop() {
    const backToTopBtn = document.querySelector('#back-to-top');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });

        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Scroll progress indicator
function initScrollProgress() {
    const progressBar = document.querySelector('#scroll-progress');
    
    if (progressBar) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const documentHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrollPercent = (scrollTop / documentHeight) * 100;
            
            progressBar.style.width = scrollPercent + '%';
        });
    }
}

// Enhanced page interactions for articles and pages
function initPageEnhancements() {
    // Add copy code functionality
    initCodeCopy();
    
    // Add image lightbox
    initImageLightbox();
    
    // Add reading progress for articles
    initReadingProgress();
    
    // Add smooth scrolling for anchor links
    initSmoothScrolling();
    
    // Add keyboard navigation
    initKeyboardNavigation();
}

// Copy code blocks functionality
function initCodeCopy() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        const wrapper = block.closest('pre');
        if (wrapper) {
            const copyButton = document.createElement('button');
            copyButton.className = 'copy-code-btn';
            copyButton.innerHTML = '📋 Копировать';
            copyButton.setAttribute('aria-label', 'Копировать код');
            
            wrapper.style.position = 'relative';
            wrapper.appendChild(copyButton);
            
            copyButton.addEventListener('click', async () => {
                try {
                    await navigator.clipboard.writeText(block.textContent);
                    copyButton.innerHTML = '✅ Скопировано!';
                    copyButton.style.background = '#10b981';
                    
                    setTimeout(() => {
                        copyButton.innerHTML = '📋 Копировать';
                        copyButton.style.background = '';
                    }, 2000);
                } catch (err) {
                    copyButton.innerHTML = '❌ Ошибка';
                    setTimeout(() => {
                        copyButton.innerHTML = '📋 Копировать';
                    }, 2000);
                }
            });
        }
    });
}

// Image lightbox functionality
function initImageLightbox() {
    const images = document.querySelectorAll('.article-content img');
    
    images.forEach(img => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', () => {
            createLightbox(img);
        });
    });
}

function createLightbox(img) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <img src="${img.src}" alt="${img.alt}" />
            <button class="lightbox-close" aria-label="Закрыть">&times;</button>
        </div>
    `;
    
    document.body.appendChild(lightbox);
    document.body.style.overflow = 'hidden';
    
    // Close lightbox
    const closeBtn = lightbox.querySelector('.lightbox-close');
    const closeLightbox = () => {
        document.body.removeChild(lightbox);
        document.body.style.overflow = '';
    };
    
    closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeLightbox();
    });
}

// Reading progress for articles
function initReadingProgress() {
    const article = document.querySelector('.article-content');
    if (!article) return;
    
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    document.body.appendChild(progressBar);
    
    function updateProgress() {
        const articleTop = article.offsetTop;
        const articleHeight = article.offsetHeight;
        const viewportHeight = window.innerHeight;
        const scrolled = window.scrollY - articleTop + viewportHeight;
        const progress = Math.min(Math.max(scrolled / articleHeight, 0), 1);
        
        progressBar.style.width = `${progress * 100}%`;
    }
    
    window.addEventListener('scroll', updateProgress);
    updateProgress();
}

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Keyboard navigation
function initKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        // Arrow key navigation for articles
        if (e.key === 'ArrowLeft') {
            const prevLink = document.querySelector('.nav-link.prev');
            if (prevLink) {
                window.location.href = prevLink.href;
            }
        } else if (e.key === 'ArrowRight') {
            const nextLink = document.querySelector('.nav-link.next');
            if (nextLink) {
                window.location.href = nextLink.href;
            }
        } else if (e.key === 'Home' && e.ctrlKey) {
            e.preventDefault();
            window.location.href = 'index.html';
        }
    });
}

// Performance optimization
function initPerformanceOptimizations() {
    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Preload critical resources
    const criticalLinks = document.querySelectorAll('a[href$=".html"]');
    criticalLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            if (!link.dataset.preloaded) {
                const preloadLink = document.createElement('link');
                preloadLink.rel = 'prefetch';
                preloadLink.href = link.href;
                document.head.appendChild(preloadLink);
                link.dataset.preloaded = 'true';
            }
        });
    });
}

// ПРОСТАЯ И НАДЕЖНАЯ MASONRY ФУНКЦИЯ
function initMasonryLayout() {
    const grids = document.querySelectorAll('.projects-grid');
    
    grids.forEach(grid => {
        const cards = grid.querySelectorAll('.project-card:not([style*="display: none"])');
        
        // Сброс всех предыдущих стилей
        cards.forEach(card => {
            card.style.gridRowEnd = '';
        });
        
        // Получаем значения из CSS
        const computedStyle = getComputedStyle(grid);
        const rowHeight = parseInt(computedStyle.gridAutoRows) || 10;
        const gap = parseInt(computedStyle.gap) || 32;
        
        // Функция для расчета высоты одной карточки
        function calculateCardSpan(card) {
            // Временно убираем grid-row-end для получения естественной высоты
            card.style.gridRowEnd = 'auto';
            
            // Принудительный reflow
            grid.offsetHeight;
            
            // Получаем высоту карточки
            const cardHeight = card.offsetHeight;
            
            // Рассчитываем количество строк
            const rowSpan = Math.ceil((cardHeight + gap) / (rowHeight + gap));
            
            // Устанавливаем grid-row-end
            const finalSpan = Math.max(1, rowSpan);
            card.style.gridRowEnd = `span ${finalSpan}`;
            
            // Отладка
            if (window.location.search.includes('debug')) {
                console.log(`Card height: ${cardHeight}px, Row span: ${finalSpan}`);
            }
        }
        
        // Ждем полного рендеринга
        setTimeout(() => {
            cards.forEach(calculateCardSpan);
        }, 100);
        
        // Обработчик изменения размера окна
        let resizeTimeout;
        function handleResize() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                cards.forEach(calculateCardSpan);
            }, 150);
        }
        
        // Удаляем старые обработчики и добавляем новый
        window.removeEventListener('resize', window.masonryResizeHandler);
        window.masonryResizeHandler = handleResize;
        window.addEventListener('resize', handleResize);
    });
}

// Keyboard navigation for general use
document.addEventListener('keydown', function(e) {
    // ESC key closes mobile menu
    if (e.key === 'Escape') {
        const navLinks = document.querySelector('.nav-links');
        const navToggle = document.querySelector('.nav-toggle');
        if (navLinks && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    }
    
    // Ctrl+K or Cmd+K focuses search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('#search');
        if (searchInput) {
            searchInput.focus();
        }
    }
});
