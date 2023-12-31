document.addEventListener("DOMContentLoaded", function () {
  const productList = document.getElementById("product-list");
  const categoryDropdown = document.getElementById("category");
  let allProducts = [];
  const itemsPerPage = 3;
  let currentPage = 1;
  let nextPage = document.querySelector("#nextPage");
  let previousPage = document.querySelector("#previousPage");

  // Assurez-vous de définir totalPages.

  // Fonction pour charger les produits et les catégories en une seule requête.
  function loadData() {
    fetch("get_catalog_data/")
      .then((response) => response.json())
      .then((data) => {
        const categories = data.categories;
        allProducts = data.products;
        totalPages = Math.ceil(allProducts.length / itemsPerPage);

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

    const totalCategoryPages = getTotalPagesForCategory(
      selectedCategory,
      allProducts
    );
    if (currentPage > totalCategoryPages) {
      currentPage = totalCategoryPages;
    }

    fetch(`get_catalog_data/?category=${selectedCategory}`)
      .then((response) => response.json())
      .then((data) => {
        let productsByCat;
        productsByCat = data.products;
        displayProducts(productsByCat);
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
    productList.innerHTML = ""; //
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const displayedProducts = products.slice(startIndex, endIndex);
    displayedProducts.forEach((product) => {
      const productDiv = document.createElement("div");

      if (product.promotion && product.promotion.status == true) {
        const formatedEndDate = formatPromotionEndDate(
          product.promotion.end_date
        );
        productDiv.innerHTML = `
                <div class="card m-auto my-2 " style="width:18rem;">
                <img class="card-img-top mt-3 p-2" src="${product.image}" alt="Card image cap" >
                <div class="card-body">
                <h5 class="card-title">              ${product.label}</h5>
                <p class="card-text">${product.description}</p>
                </div>
                <ul class="list-group list-group-flush">
                <li class="list-group-item">Catégorie : ${product.category}</li>
                <li class="list-group-item">Promotion de ${product.promotion.discount_percentage} % valable jusqu'au ${formatedEndDate}</li>
                <li class="list-group-item">Prix :<span class="promotion"> ${product.price} €</span></li>
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
          
          <li class="list-group-item">Prix :<span> ${product.price} €</span></li>
          </ul>
          </div>
                
            `;
      }

      productList.appendChild(productDiv);

      let pageCourante = document.getElementById("currentPage");
      pageCourante.textContent = currentPage;
      let lastPage = document.getElementById("lastPage");
      lastPage.addEventListener("click", () => {
        if (currentPage < totalPages) {
          currentPage = totalPages;
          loadPage(currentPage);
        }
      });
      if (totalPages == 1) {
        nextPage.style.display = "none";
        lastPage.style.display = "none";
        previousPage.style.display = "none";
      } else {
        nextPage.style.display = "list-item";
        lastPage.style.display = "list-item";
        previousPage.style.display = "list-item";
      }
    });
  }
  function formatPromotionEndDate(endDate) {
    const dateObject = new Date(endDate);
    const day = dateObject.getDate();
    const month = dateObject.getMonth() + 1;
    const year = dateObject.getFullYear();
    return `${day}/${month}/${year}`;
  }
  function loadPage(pageNumber) {
    displayProducts(allProducts);
  }
  function getTotalPagesForCategory(categoryId, products) {
    const categoryProducts = products.filter(
      (product) => product.categoryId == categoryId
    );

    let limit = Math.ceil(categoryProducts.length / itemsPerPage);
    if (categoryProducts.length != 0) {
      totalPages = limit;
    } else {
      totalPages = Math.ceil(products.length / itemsPerPage);
    }

    return totalPages;
  }

  nextPage.addEventListener("click", () => {
    if (currentPage < totalPages) {
      currentPage++;
      loadPage(currentPage);
    }
  });

  previousPage.addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      loadPage(currentPage);
    }
  });
});
