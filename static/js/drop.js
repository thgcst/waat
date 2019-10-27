var dropzone = document.getElementById("dropzone");
var body = document.body;

dropzone.ondragover = function() {
  this.className = "dropzoneB4 dragover";
  return false;
};

dropzone.ondragleave = function() {
  this.className = "dropzoneB4";
  return false;
};

document.addEventListener("drop", function(e) {
  e.preventDefault();
  e.stopPropagation();
});
document.addEventListener("dragover", function(e) {
  e.preventDefault();
  e.stopPropagation();
});

dropzone.ondrop = function(e) {
  e.preventDefault();
  deletePic();
  this.className = "dropzoneB4";
  encodeImageFileAsURL(e.dataTransfer);
};

function encodeImageFileAsURL(element) {
  var file = element.files[0];
  var reader = new FileReader();
  var foto;
  reader.onloadend = function() {
    var foto = reader.result;
    console.log(foto);
    showUploadedImage(foto, file.name);
  };
  reader.readAsDataURL(file);
}

function create(htmlStr) {
  var elem = document.createElement("div");
  elem.innerHTML = htmlStr;
  return elem;
}

function showUploadedImage(foto, nome) {
  document.getElementsByName("foto")[0].value = foto;

  var box = document.getElementById("dropzone");

  box.removeChild(box.firstChild); 
  box.removeChild(box.firstChild);
  box.removeChild(box.firstChild);
  var img = document.createElement("img");
  att = document.createAttribute("src");
  att.value = foto;
  img.setAttributeNode(att);
  att = document.createAttribute("class");
  att.value = "foto";
  img.setAttributeNode(att);
  att = document.createAttribute("value");
  att.value = foto;

  // box.appendChild(img);

  box.appendChild(
    create(
      "<div class='boxNome' id='boxe'><a id='nomeFoto' style='color: #888; padding-bottom: 5px' name='foto'></a></div>"
    )
  );
  t = document.createTextNode(nome);
  document.getElementById("nomeFoto").setAttributeNode(att);
  document.getElementById("nomeFoto").appendChild(t);
  document
    .getElementById("boxe")
    .appendChild(create('<i class="fas fa-times-circle" onclick="deletePic()"></i>'));

  box.appendChild(img);

  dropzone.className = "dropzoneAfter";

  console.log(box);
}

function deletePic() {
  while (dropzone.hasChildNodes()) {
    dropzone.removeChild(dropzone.firstChild);
  }
  dropzone.innerHTML = "Arraste uma foto de sua assinatura<br> para gerar boletos automáticos";

  dropzone.className = "dropzoneB4";
}
