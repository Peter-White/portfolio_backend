$(document).ready(function(){
  let $displayForm = $('.displayForm');
  let $form_container = $('div#form-container');

  $displayForm.click(function(e) {
    e.preventDefault();
    $form_container.each(function() {
      if($(this).hasClass("hide")) {
        $displayForm.html('-');
        $(this).removeClass("hide");
        $(this).addClass("show");
      } else {
        $displayForm.html('+');
        $(this).removeClass("show");
        $(this).addClass("hide");
      }
    });
  });
});
