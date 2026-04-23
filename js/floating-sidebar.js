/**
 * Floating Sidebar Component
 * Adds quick contact and search tools
 */
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.createElement('div');
    sidebar.className = 'floating-sidebar';
    sidebar.innerHTML = `
        <div class="float-item search" title="產品搜尋" onclick="window.scrollTo({top: document.getElementById('products').offsetTop - 100, behavior: 'smooth'})">
            <i data-lucide="search" style="width:22px;height:22px;"></i>
        </div>
        <a href="https://line.me" target="_blank" class="float-item line" title="LINE 客服">
            <i data-lucide="message-circle" style="width:22px;height:22px;"></i>
        </a>
        <a href="mailto:jojo.li888@msa.hinet.net" class="float-item email" title="發送郵件">
            <i data-lucide="mail" style="width:22px;height:22px;"></i>
        </a>
        <div class="float-item back-to-top" title="回到頂部" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
            <i data-lucide="arrow-up" style="width:22px;height:22px;"></i>
        </div>
    `;
    
    document.body.appendChild(sidebar);
    
    // Refresh icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Scroll reveal logic for sidebar
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            sidebar.style.opacity = '1';
            sidebar.style.pointerEvents = 'all';
        } else {
            sidebar.style.opacity = '0';
            sidebar.style.pointerEvents = 'none';
        }
    });

    // Initial state
    sidebar.style.opacity = '0';
    sidebar.style.pointerEvents = 'none';
    sidebar.style.transition = 'opacity 0.3s ease';
});
