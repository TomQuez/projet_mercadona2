document.addEventListener("DOMContentLoaded", function () {
  const productList = document.getElementById("product-list");
  const categoryDropdown = document.getElementById("category");

  let allProducts = []; // Pour conserver tous les produits d'origine.

  fetch("get_catalog_data/")
    .then((response) => response.json())
    .then((data) => {
      allProducts = data.products; // Conservez tous les produits d'origine.

      // Remplissez le menu déroulant des catégories.
      const uniqueCategories = [
        ...new Set(allProducts.map((product) => product.category)),
      ];
      uniqueCategories.forEach((category) => {
        const option = document.createElement("option");
        option.value = category;
        option.textContent = category;
        categoryDropdown.appendChild(option);
      });

      // Affichez tous les produits au chargement initial.
      displayProducts(allProducts);

      // Ajoutez un gestionnaire d'événements pour le changement de catégorie.
      categoryDropdown.addEventListener("change", function () {
        const selectedCategory = categoryDropdown.value;
        const filteredProducts = filterProductsByCategory(
          allProducts,
          selectedCategory
        );
        displayProducts(filteredProducts);
      });
    })
    .catch((error) => {
      console.error(
        "Une erreur s'est produite lors de la récupération des données :",
        error
      );
    });

  // Fonction pour afficher les produits dans le catalogue.
  function displayProducts(products) {
    productList.innerHTML = ""; // Effacez le contenu précédent.

    products.forEach((product) => {
      const productDiv = document.createElement("div");

      // productDiv.classList.add("row");

      if (product.promotion && product.promotion.status == true) {
        productDiv.innerHTML = `
              <div class="card m-auto my-2 " style="width:18rem;">
              <img class="card-img-top mt-3 p-2" src="${product.image}" alt="Card image cap" >
              <div class="card-body">
              <h5 class="card-title">              ${product.label}</h5>
              <p class="card-text">${product.description}</p>
              </div>
              <ul class="list-group list-group-flush">
              <li class="list-group-item">Catégorie : ${product.category}</li>
              <li class="list-group-item">Promotion de ${product.promotion.discount_percentage} % valable jusqu'au ${product.promotion.end_date}</li>
              <li class="list-group-item">Prix :<span class="promotion"> ${product.price}</span></li>
              </ul>
              </div>
                           
          `;
      } else {
        productDiv.innerHTML = `
        <div class="card m-auto mt-2" style="width:18rem;">
        <img class="card-img-top mt-3" src="${product.image}" alt="Card image cap">
        <div class="card-body">
        <h5 class="card-title">              ${product.label}</h5>
        <p class="card-text">${product.description}</p>
        </div>
        <ul class="list-group list-group-flush">
        <li class="list-group-item">Catégorie : ${product.category}</li>
        
        <li class="list-group-item">Prix :<span> ${product.price}</span></li>
        </ul>
        </div>
              
          `;
      }

      productList.appendChild(productDiv);
    });
  }

  // Fonction pour filtrer les produits par catégorie.
  function filterProductsByCategory(products, category) {
    if (!category) {
      return products; // Retournez tous les produits si aucune catégorie n'est sélectionnée.
    }

    return products.filter((product) => product.category === category);
  }
});
