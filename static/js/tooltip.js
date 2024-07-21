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
        tooltip.classList.remove('top-tooltip', 'right-tooltip')
    });
};

function adaptTooltip(tooltip) {
    const tooltipText = tooltip.querySelector('.tooltip-text');
    const tooltipRect = tooltipText.getBoundingClientRect();

    if (tooltipRect.top - 5 < 0) {
        tooltip.classList.add('top-tooltip');
    }

    if (tooltipRect.right + 5 > window.innerWidth) {
        tooltip.classList.add('right-tooltip');
    }
};