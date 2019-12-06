$(document).ready(function(){
  let url = window.location.href.split("/");

  let $overlay = $("#overlay");
  let $card = $(".card");
  let $cardImg = $(".card-img-top");
  let $btnDanger = $(".btn-danger");
  let $cardTitle = $("card-title");
  let $skill = $("li#skill");
  let projectId = parseInt(url[url.length - 1]);
  let $image = "";
  let imgId = -1;

  $("img").click(function(){
    $overlay.addClass("show");
    $cardImg.attr("src", $(this).attr("src"));
    imgId = $(this).attr("class");
    $image = $(this);
  });

  $overlay.click(function(){
    $overlay.removeClass("show");
  });

  $card.click(function(e){
    e.stopPropagation();
  });

  $btnDanger.click(function(){
    $.post("/deleteimage/" + imgId, function(data){
      if (Object.keys(data)[0] === "success") {
        imgId = -1;
        image = "";
        $overlay.removeClass("show");
        $image.parent().remove();
        $cardTitle.text() = "";
      } else {
        $cardTitle.text() = data[Object.keys(data)[0]];
      }
    });
  });

  $skill.click(function() {
    let skill = $(this);
    if(confirm("Are you sure you want to remove this skill from this project?")) {
      $.post("/deleteprojectskill?skill=" + $(this).attr("class") + "&project=" + projectId, function(data){
        if (Object.keys(data)[0] === "success") {
          skill.remove();
        } else {
          alert(data[Object.keys(data)[0]]);
        }
      });
    }
  });
});
