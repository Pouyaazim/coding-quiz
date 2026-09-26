/* ============================================
   AWWWARDS-LEVEL ANIMATIONS
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ==================== SCROLL REVEAL ====================
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-scale, .stagger');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.05,
        rootMargin: '0px 0px -30px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // Safety net: اگه تا ۱.۵ ثانیه چیزی revealed نشد، همه رو نشون بده
    setTimeout(() => {
        revealElements.forEach(el => {
            if (!el.classList.contains('revealed')) {
                const rect = el.getBoundingClientRect();
                if (rect.top < window.innerHeight + 100) {
                    el.classList.add('revealed');
                }
            }
        });
    }, 1500);

    // On scroll fallback for elements below fold
    let scrollTimer = null;
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(() => {
            revealElements.forEach(el => {
                if (!el.classList.contains('revealed')) {
                    const rect = el.getBoundingClientRect();
                    if (rect.top < window.innerHeight - 30) {
                        el.classList.add('revealed');
                    }
                }
            });
        }, 100);
    }, { passive: true });

    // ==================== 3D TILT ====================
    const tiltCards = document.querySelectorAll('.tilt-card');

    tiltCards.forEach(card => {
        let rafId = null;

        card.addEventListener('mousemove', (e) => {
            if (rafId) cancelAnimationFrame(rafId);

            rafId = requestAnimationFrame(() => {
                const rect = card.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width;
                const y = (e.clientY - rect.top) / rect.height;

                const tiltX = (y - 0.5) * -10;
                const tiltY = (x - 0.5) * 10;

                card.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale(1.02)`;
                card.style.setProperty('--glare-x', `${x * 100}%`);
                card.style.setProperty('--glare-y', `${y * 100}%`);
            });
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)';
        });
    });

    // ==================== COUNTER ANIMATION ====================
    const counters = document.querySelectorAll('[data-counter]');

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.dataset.counter, 10) || 0;
                const duration = 1200;
                const start = performance.now();

                const animate = (now) => {
                    const progress = Math.min((now - start) / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3);
                    el.textContent = Math.floor(eased * target).toLocaleString('fa-IR');
                    if (progress < 1) requestAnimationFrame(animate);
                };

                requestAnimationFrame(animate);
                counterObserver.unobserve(el);
            }
        });
    }, { threshold: 0.3 });

    counters.forEach(el => counterObserver.observe(el));

    // Safety: اگه تا ۲ ثانیه counter انیمیت نشد، مقدار مستقیم بذار
    setTimeout(() => {
        counters.forEach(el => {
            if (el.textContent === '0') {
                const target = parseInt(el.dataset.counter, 10) || 0;
                el.textContent = target.toLocaleString('fa-IR');
            }
        });
    }, 2000);

    // ==================== RIPPLE ON CLICK ====================
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height);

            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${e.clientX - rect.left - size/2}px;
                top: ${e.clientY - rect.top - size/2}px;
                background: rgba(255,255,255,0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: rippleEffect 0.6s ease-out;
                pointer-events: none;
            `;

            if (getComputedStyle(this).position === 'static') {
                this.style.position = 'relative';
            }
            this.style.overflow = 'hidden';

            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
});

// Ripple keyframe
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes rippleEffect {
        to { transform: scale(2.5); opacity: 0; }
    }
`;
document.head.appendChild(rippleStyle);