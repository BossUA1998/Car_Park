// static/js/main.js

document.addEventListener("DOMContentLoaded", () => {
    const shapes = document.querySelectorAll('.shape');
    let mouseX = 0;
    let mouseY = 0;
    let isParallaxRunning = false;

    // Слухач подій лише оновлює координати (це дуже швидко)
    document.addEventListener("mousemove", (e) => {
        mouseX = e.pageX;
        mouseY = e.pageY;

        if (!isParallaxRunning) {
            requestAnimationFrame(updateParallax);
            isParallaxRunning = true;
        }
    });

    // Функція анімації виконується синхронно з оновленням екрану
    function updateParallax() {
        const width = window.innerWidth;
        const height = window.innerHeight;

        shapes.forEach(layer => {
            const speed = parseFloat(layer.getAttribute('data-speed')) || 2;

            // Розрахунок зсуву
            const x = (width - mouseX * speed) / 100;
            const y = (height - mouseY * speed) / 100;

            layer.style.transform = `translate(${x}px, ${y}px)`;
        });

        isParallaxRunning = false;
    }

    console.log("Dashboard scripts loaded (Optimized).");
});