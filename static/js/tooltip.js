document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll(".tooltip-container").forEach(function(tooltip) {
        tooltip.addEventListener('mouseenter', (event) => {
            resetTooltips();
            adaptTooltip(event.target);
        });
    });
});

function resetTooltips() {
    document.querySelectorAll('.tooltip-container').forEach((tooltip) => {
        tooltip.classList.remove('top-tooltip', 'right-tooltip', 'left-tooltip')
    });
};

function adaptTooltip(tooltip) {
    const tooltipText = tooltip.querySelector('.tooltip-text');
    const tooltipRect = tooltipText.getBoundingClientRect();
    const sidebarRectLeft = document.querySelector('#sidebar').getBoundingClientRect().left;

    if (tooltipRect.top - 5 < 0) {
        tooltip.classList.add('top-tooltip');
    }

    if (tooltipRect.right + 5 > window.innerWidth) {
        tooltip.classList.add('right-tooltip');
    }

    if (tooltipRect.left - 5 < sidebarRectLeft) {
        tooltip.classList.add('left-tooltip');
    }
};