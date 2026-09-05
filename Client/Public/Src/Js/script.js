document.addEventListener("DOMContentLoaded", () => {
    // Register GSAP Plugins
    gsap.registerPlugin(ScrollTrigger);

    // --- Hero Animation Sequence ---
    const heroTimeline = gsap.timeline({ defaults: { ease: "power3.out" } });

    heroTimeline
        .to(".hero-image", {
            opacity: 1,
            scale: 1,
            rotation: 0,
            duration: 1.5,
            delay: 0.2
        })
        .to(".hero-details .title", {
            opacity: 1,
            y: 0,
            duration: 1
        }, "-=1")
        .to(".hero-details .subtitle", {
            opacity: 1,
            y: 0,
            duration: 1
        }, "-=0.8")
        .to(".hero-details .description", {
            opacity: 1,
            y: 0,
            duration: 1
        }, "-=0.8")
        .to(".buttons", {
            opacity: 1,
            y: 0,
            duration: 1
        }, "-=0.8");

    // --- Parallax Effect for Menu Items ---
    gsap.utils.toArray(".menu-item").forEach((item, i) => {
        gsap.from(item, {
            scrollTrigger: {
                trigger: item,
                start: "top bottom-=100",
                toggleActions: "play none none reverse"
            },
            y: 100,
            opacity: 0,
            duration: 0.8,
            delay: i * 0.1 // Stagger effect
        });
    });

    // --- Navbar Scroll Effect ---
    const header = document.querySelector("header");
    let lastScroll = 0;

    window.addEventListener("scroll", () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll <= 0) {
            header.style.transform = "translateY(0)";
            header.style.background = "rgba(78, 52, 46, 0.95)";
        } else if (currentScroll > lastScroll) {
            // Scrolling down
            header.style.transform = "translateY(-100%)";
        } else {
            // Scrolling up
            header.style.transform = "translateY(0)";
            header.style.background = "rgba(78, 52, 46, 0.98)"; // Solid on scroll up
        }
        lastScroll = currentScroll;
    });

    // --- Mobile Menu Logic (Preserved & Enhanced) ---
    const menuOpenButton = document.querySelector("#menu-open-button");
    const menuCloseButton = document.querySelector("#menu-close-button");
    const navLinks = document.querySelectorAll(".nav-link");

    if (menuOpenButton) {
        menuOpenButton.addEventListener("click", () => {
            document.body.classList.add("show-mobile-menu");
        });
    }

    if (menuCloseButton) {
        menuCloseButton.addEventListener("click", () => {
            document.body.classList.remove("show-mobile-menu");
        });
    }

    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            document.body.classList.remove("show-mobile-menu");
        });
    });
    // --- Additive Animations ---

    // 1. Reveal Sections on Scroll
    const sections = gsap.utils.toArray('section');
    sections.forEach(section => {
        gsap.from(section.children, {
            scrollTrigger: {
                trigger: section,
                start: "top 80%",
                toggleActions: "play none none reverse"
            },
            y: 50,
            opacity: 0,
            duration: 1,
            stagger: 0.2,
            ease: "power3.out"
        });
    });

    // 2. Parallax for About Image
    gsap.to(".about-image", {
        scrollTrigger: {
            trigger: ".about-section",
            start: "top bottom",
            end: "bottom top",
            scrub: 1
        },
        y: -50,
        ease: "none"
    });

    // 3. Gallery Stagger Reveal
    gsap.from(".gallery-item", {
        scrollTrigger: {
            trigger: ".gallery-section",
            start: "top 85%"
        },
        scale: 0.8,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: "back.out(1.7)"
    });

    // 4. Initialize Swiper for Testimonials (if not already initialized)
    // Note: Ensure Swiper script is loaded in HTML
    if (typeof Swiper !== 'undefined') {
        new Swiper('.slider-wrapper', {
            loop: true,
            grabCursor: true,
            spaceBetween: 30,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                dynamicBullets: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                0: { slidesPerView: 1 },
                768: { slidesPerView: 2 },
                1024: { slidesPerView: 3 }
            }
        });
    }
});