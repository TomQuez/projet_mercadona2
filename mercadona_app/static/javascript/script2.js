document.addEventListener("DOMContentLoaded", function () {
  const productList = document.getElementById("product-list");
  const categoryDropdown = document.getElementById("category");
  let allProducts = [];
  let currentPage = 1;
  let totalPages = 1; // Assurez-vous de définir totalPages.

  // Fonction pour charger les produits et les catégories en une seule requête.
  function loadData() {
    fetch("get_catalog_data/")
      .then((response) => response.json())
      .then((data) => {
        const categories = data.categories;
        allProducts = data.products;
        totalPages = data.total_pages;
        // Remplissez le menu déroulant des catégories.
        categories.forEach((category) => {
          const option = document.createElement("option");
          option.value = category.id;
          option.textContent = category.name;
          categoryDropdown.appendChild(option);
        });
        displayProducts(allProducts); // Chargez les produits initialement.
      })
      .catch((error) => {
        console.error("Une erreur est survenue : ", error);
      });
  }

  // Gérez le changement de catégorie.
  categoryDropdown.addEventListener("change", function () {
    const selectedCategory = categoryDropdown.value;
    fetch(`get_catalog_data/?category=${selectedCategory}`)
      .then((response) => response.json())
      .then((data) => {
        allProducts = data.products;
        displayProducts(allProducts);
      })
      .catch((error) => {
        console.error(
          "une erreur est survenue durant la récupération des données :",
          error
        );
      });
  });

  // Chargez la page initiale au chargement de la page.
  loadData();

  // Fonction pour afficher les produits dans le catalogue.
  function displayProducts(products) {
    productList.innerHTML = ""; // Effacez le contenu précédent.

    products.forEach((product) => {
      const productDiv = document.createElement("div");

      // productDiv.classList add("row");

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

  // function loadPage(page) {
  //   fetch(`get_catalog_data/?page=${page}`)
  //     .then((response) => response.json())
  //     .then((data) => {
  //       displayProducts(data.products);
  //       currentPage = page;
  //       totalPages = data.total_pages;
  //     })
  //     .catch((error) => {
  //       console.error(
  //         "Une erreur est survenue pendant la récupération des données : ",
  //         error
  //       );
  //     });
  // }

  document.querySelector("#nextPage").addEventListener("click", () => {
    if (currentPage < totalPages) {
      loadPage(currentPage + 1);
    }
  });
  document.querySelector("#previousPage").addEventListener("click", () => {
    if (currentPage > 1) {
      loadPage(currentPage - 1);
    }
  });
  // function filterProductsByCategory(products, category) {
  //   if (!category) {
  //     return products;
  //   }
  //   return products.filter((product) => product.category === category);
  // }
});
