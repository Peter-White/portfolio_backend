$(document).ready(function(){

  let $deleteImage = $("a.btn.btn-danger.deleteImage");

  $deleteImage.click(function(e) {
    e.preventDefault();

    console.log($(this));
  });
});
