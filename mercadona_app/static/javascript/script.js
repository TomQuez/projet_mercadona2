// Utilisez Fetch pour récupérer les données JSON de votre vue Django
fetch("get_catalog_data/") // Assurez-vous que l'URL correspond à l'URL de votre vue Django
  .then((response) => response.json())
  .then((data) => {
    const products = data.products;
    const productList = document.getElementById("product-list");

    // Créez le contenu HTML pour afficher les produits
    products.forEach((product) => {
      const productDiv = document.createElement("div");
      //   productDiv.classList.add("product-item");

      productDiv.innerHTML = `
              <h2>${product.label}</h2>
              <p>Prix : ${product.price} €</p>
              <p>Description : ${product.description}</p>
              <p>Catégorie : ${product.category}</p>
              <img src="${product.image}" alt="${product.label}" style='width:300px;height:auto;'>
          `;

      productList.appendChild(productDiv);
    });
  })
  .catch((error) => {
    console.error(
      "Une erreur s'est produite lors de la récupération des données :",
      error
    );
  });
