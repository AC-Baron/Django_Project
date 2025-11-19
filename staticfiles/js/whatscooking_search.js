document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('whatscooking-search');
  const recipeGrid = document.getElementById('whatscooking-grid');

  if (!searchInput || !recipeGrid) return;

  const recipeCards = recipeGrid.querySelectorAll('.recipe-card');

  console.log("✅ What's Cooking search ready");

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase().trim();
    let visibleCount = 0;

    recipeCards.forEach(card => {
      const title = card.dataset.title || '';
      const ingredients = card.dataset.ingredients || '';

      if (title.includes(query) || ingredients.includes(query)) {
        card.style.display = 'block';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    // "No results" message
    let noResultsMsg = document.getElementById('no-results-msg');
    if (!noResultsMsg) {
      noResultsMsg = document.createElement('p');
      noResultsMsg.id = 'no-results-msg';
      noResultsMsg.textContent = 'No recipes match your search.';
      noResultsMsg.style.textAlign = 'center';
      noResultsMsg.style.marginTop = '20px';
      noResultsMsg.style.display = 'none';
      recipeGrid.insertAdjacentElement('afterend', noResultsMsg);
    }

    noResultsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
  });
});
