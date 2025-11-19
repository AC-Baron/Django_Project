document.addEventListener('DOMContentLoaded', function () {
  // Collapsible code (keep it as you had)
  document.querySelectorAll('.collapse-btn').forEach(button => {
    button.addEventListener('click', () => {
      const target = document.querySelector(button.dataset.target);
      const isVisible = target.style.display === 'block';
      target.style.display = isVisible ? 'none' : 'block';
      button.textContent = button.textContent.replace(isVisible ? '▲' : '▼', isVisible ? '▼' : '▲');
    });
  });

  // --- Search Functionality ---
  const searchInput = document.getElementById('cookbook-search');
  if (!searchInput) return;

  console.log("✅ Cookbook search initialized (robust)");

  // Select all recipe-card elements in both grids
  const recipeCards = document.querySelectorAll(
    '#my-recipes-grid .recipe-card, #favourite-recipes-grid .recipe-card'
  );

  // Helper to show/hide either the card or its wrapper (if present)
  function setVisible(card, visible) {
    const wrapper = card.closest('.recipe-card-wrapper');
    if (wrapper) {
      wrapper.style.display = visible ? '' : 'none';
    } else {
      // keep layout type (flex) when visible; hide when not
      card.style.display = visible ? '' : 'none';
    }
  }

  // Initially ensure all are visible
  recipeCards.forEach(c => setVisible(c, true));

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase().trim();

    // If query empty -> show everything
    if (!query) {
      recipeCards.forEach(card => setVisible(card, true));
      return;
    }

    recipeCards.forEach(card => {
      // Prefer dataset if present, fallback to DOM text
      const title = (card.dataset.title && card.dataset.title.toLowerCase()) ||
                    (card.querySelector('.recipe-title')?.textContent.toLowerCase() || '');

      const ingredients = (card.dataset.ingredients && card.dataset.ingredients.toLowerCase()) ||
                          (card.querySelector('.recipe-ingredients')?.textContent.toLowerCase() || '');

      const matches = title.includes(query) || ingredients.includes(query);

      setVisible(card, matches);
    });
  });
});
