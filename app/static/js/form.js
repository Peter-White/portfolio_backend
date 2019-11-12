$(document).ready(function(){
  let $displayForm = $('.displayForm');
  let $form_container = $('#form-container');

  $displayForm.click(function(e) {
    e.preventDefault();
    if($form_container.hasClass("hide")) {
      $displayForm.html('-');
      $form_container.removeClass("hide");
      $form_container.addClass("show");
    } else {
      $displayForm.html('+');
      $form_container.removeClass("show");
      $form_container.addClass("hide");
    }
  });
});
