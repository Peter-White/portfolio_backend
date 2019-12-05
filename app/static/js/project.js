$(document).ready(function(){
  let $overlay = $("#overlay");
  let $card = $(".card");
  let $cardImg = $(".card-img-top");

  // $("img").click(function(){ console.log($(this).attr("src")); });
  $("img").click(function(){
    $overlay.addClass("show");
    $cardImg.attr("src", $(this).attr("src"));
  });
  $overlay.click(function(){
    $overlay.removeClass("show");
  });
  $card.click(function(e){
    e.stopPropagation();
  });
});
