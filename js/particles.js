/* ============================================================
   Premium Particle Background System
   High-performance Canvas animation for Hero Section
   ============================================================ */
class ParticleSystem {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.particleCount = window.innerWidth < 768 ? 15 : 80;
        this.mouse = { x: null, y: null, radius: 150 };
        
        this.config = {
            color: '212, 168, 67', // Industrial Gold
            lineOpacity: 0.15,
            particleOpacity: 0.3
        };

        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
        });
        window.addEventListener('mouseleave', () => {
            this.mouse.x = null;
            this.mouse.y = null;
        });
        
        this.resize();
        this.createParticles();
        this.animate();
    }
    
    resize() {
        const parent = this.canvas.parentElement;
        this.canvas.width = parent.clientWidth;
        this.canvas.height = parent.clientHeight;
    }
    
    createParticles() {
        this.particles = [];
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 2 + 1,
                speedX: (Math.random() - 0.5) * 0.4,
                speedY: (Math.random() - 0.5) * 0.4,
            });
        }
    }
    
    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        for (let i = 0; i < this.particles.length; i++) {
            let p = this.particles[i];
            
            // Move
            p.x += p.speedX;
            p.y += p.speedY;
            
            // Bounds
            if (p.x < 0 || p.x > this.canvas.width) p.speedX *= -1;
            if (p.y < 0 || p.y > this.canvas.height) p.speedY *= -1;
            
            // Mouse Influence
            if (this.mouse.x && this.mouse.y) {
                let dx = this.mouse.x - p.x;
                let dy = this.mouse.y - p.y;
                let dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < this.mouse.radius) {
                    let force = (this.mouse.radius - dist) / this.mouse.radius;
                    p.x -= dx * force * 0.03;
                    p.y -= dy * force * 0.03;
                }
            }

            // Draw Particle
            this.ctx.fillStyle = `rgba(${this.config.color}, ${this.config.particleOpacity})`;
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fill();

            // Draw Connections
            for (let j = i + 1; j < this.particles.length; j++) {
                let p2 = this.particles[j];
                let dx = p.x - p2.x;
                let dy = p.y - p2.y;
                let dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist < 150) {
                    let opacity = (1 - (dist / 150)) * this.config.lineOpacity;
                    this.ctx.strokeStyle = `rgba(${this.config.color}, ${opacity})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.beginPath();
                    this.ctx.moveTo(p.x, p.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.stroke();
                }
            }
        }
    }
    
    animate() {
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
}

// Global initialization
window.initHeroParticles = (id) => new ParticleSystem(id);

document.addEventListener('DOMContentLoaded', () => {
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        window.initHeroParticles('hero-canvas');
    }
});
