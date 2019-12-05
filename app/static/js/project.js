$(document).ready(function(){
  let $overlay = $("#overlay");
  let $card = $(".card");

  // $("img").click(function(){ console.log($(this).attr("src")); });
  $("img").click(function(){
    $overlay.addClass("show");
  });
  $overlay.click(function(){
    $overlay.removeClass("show");
  });
  $card.click(function(e){
    e.stopPropagation();
  });
});
