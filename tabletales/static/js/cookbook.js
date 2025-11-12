document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.collapse-btn').forEach(button => {
    button.addEventListener('click', () => {
      const target = document.querySelector(button.dataset.target);
      const isVisible = target.style.display === 'block';
      target.style.display = isVisible ? 'none' : 'block';
      button.textContent = button.textContent.replace(isVisible ? '▲' : '▼', isVisible ? '▼' : '▲');
    });
  });
});
