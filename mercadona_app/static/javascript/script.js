fetch("get_catalog_data/")
  .then((response) => response.json())
  .then((data) => {
    const products = data.products;
    const productList = document.getElementById("product-list");

    products.forEach((product) => {
      const productDiv = document.createElement("div");
      productDiv.classList.add("row");
      // productDiv.classList.add("justify content-center");

      if (product.promotion && product.promotion.status == true) {
        productDiv.innerHTML = `
              <div class="card m-auto mt-2" style="width:18rem;">
              <img class="card-img-top mt-3" src="${product.image}" alt="Card image cap">
              <div class="card-body">
              <h5 class="card-title">              ${product.label}</h5>
              <p class="card-text">${product.description}</p>
              </div>
              <ul class="list-group list-group-flush">
              <li class="list-group-item">catégorie : ${product.category}</li>
              <li class="list-group-item">promotion de ${product.promotion.discount_percentage} valable jusqu'au ${product.promotion.end_date}</li>
              <li class="list-group-item">prix :<span class="promotion"> ${product.price}</span></li>
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
        <li class="list-group-item">catégorie : ${product.category}</li>
        
        <li class="list-group-item">prix :<span> ${product.price}</span></li>
        </ul>
        </div>
              
          `;
      }

      productList.appendChild(productDiv);
    });
  })
  .catch((error) => {
    console.error(
      "Une erreur s'est produite lors de la récupération des données :",
      error
    );
  });
