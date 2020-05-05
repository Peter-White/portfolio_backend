$(document).ready(function(){
  let url = window.location.href.split("/");

  let $btnDanger = $(".btn-danger");
  let projectId = parseInt(url[url.length - 1]);

  $(document.body).on('click', 'li#skill', function() {
    let skill = $(this);
    if(confirm("Are you sure you want to remove this skill from this project?")) {
      $.post("/deleteprojectskill?skill=" + $(this).attr("class") + "&project=" + projectId, function(data){
        if (Object.keys(data)[0] === "success") {
          let $categoryMenu = $("div#" + data[Object.keys(data)[0]]["category"]);
          $categoryMenu.append('<button id=' + data[Object.keys(data)[0]]["id"] + ' class="dropdown-item" type="button">' + data[Object.keys(data)[0]]["title"] + '</button>');
          skill.remove();
        } else {
          alert(data[Object.keys(data)[0]]);
        }
      });
    }
  });

  $(document.body).on('click', 'button.dropdown-item', function() {
    let $button = $(this);
    $.post("/addprojectskill?skill=" + $(this).attr("id") + "&project=" + projectId, function(data){
      if (Object.keys(data)[0] === "success") {
        let $categoryList = $("ul." + data[Object.keys(data)[0]]["category"]);
        $categoryList.append('<li id="skill" class=' + data[Object.keys(data)[0]]["id"] + '>' + data[Object.keys(data)[0]]["title"] + '<span class="deleteX">✘</span></li>')
        $button.remove();
      } else {
        alert(data[Object.keys(data)[0]]);
      }
    });
  });
});
