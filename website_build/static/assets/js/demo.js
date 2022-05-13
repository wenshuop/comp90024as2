/* Team 13, Melbourne
Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au */

document.addEventListener("DOMContentLoaded", function (event) {
  let img_box = document.querySelector(".img_box");
  let imgs = document.querySelectorAll("img");
  let sel_box = document.querySelector(".sel_box");
  let lis = sel_box.querySelectorAll("li");
  let left_btn = document.querySelector(".left_btn");
  let right_btn = document.querySelector(".right_btn");

  // Record the index of picture
  let index = 0;
  let timer = null;
  // Set the size of image container
  let imgContainerW = img_box.offsetWidth;
  img_box.style.width = imgContainerW * imgs.length + "px";
  // Set the position of image container
  img_box.style.left = 0 + "px";

  console.log(imgContainerW, img_box.style.width, img_box.style.left);
  // Set the first image as the current button
  lis[0].className = "cur";

  function swapImg() {
    img_box.style.left = -index * imgContainerW + "px";
    for (let i = 0; i < lis.length; i++) {
      lis[i].className = "";
    }
    lis[index].className = "cur";
  }

  function swapFormat() {
    index++;
    if (index >= 4) {
      index = 4;
      img_box.style.transition = "all, linear, 1s";
      img_box.style.left = -index * imgContainerW + "px";
      for (let i = 0; i < lis.length; i++) {
        lis[i].className = "";
      }
      lis[0].className = "cur";

      // When the image transition is finished, it immediately switches to the first image by using the delaying timer.
      setTimeout(function () {
        index = 0;
        img_box.style.transition = "";
        swapImg();
      }, 1500);

      // Otherwise, transit pictures normally
    } else {
      img_box.style.transition = "all, linear, 1.5s";
      swapImg();
    }
  }

  timer = setInterval(swapFormat, 3000);


  right_btn.addEventListener("click", function () {
    swapFormat();
  });


  left_btn.addEventListener("click", function () {
    index--;
    if (index < 0) {
      index = -1;
      img_box.style.transition = "all, linear, 1.5s";
      img_box.style.left = -index * imgContainerW + "px";
      for (let i = 0; i < lis.length; i++) {
        lis[i].className = "";
      }
      lis[3].className = "cur";


      setTimeout(function () {
        index = 3;
        img_box.style.transition = "";
        swapImg();
      }, 1000);
    } else {
      img_box.style.transition = "all, linear, 1.5s";
      swapImg();
    }
  });

  // Clear the timer when the mouse is over the picture, left arrow, right arrow, i.e. the picture is not rotated
  img_box.addEventListener("mouseover", function () {
    clearInterval(timer);
  });

  right_btn.addEventListener("mouseover", function () {
    clearInterval(timer);
  });

  left_btn.addEventListener("mouseover", function () {
    clearInterval(timer);
  });

  // Turn on the timer when the mouse leaves the picture, left arrow, right arrow, that is, the picture continues to rotate
  img_box.addEventListener("mouseout", function () {
    timer = setInterval(swapFormat, 3000);
  });

  left_btn.addEventListener("mouseout", function () {
    timer = setInterval(swapFormat, 3000);
  });

  right_btn.addEventListener("mouseout", function () {
    timer = setInterval(swapFormat, 3000);
  });

  sel_box.addEventListener("click", function (e) {
    e.preventDefault();
    if (e.target.tagName.toLowerCase() === "li") {
      const i = e.target.getAttribute("data-index");
      index = Number(i);
      img_box.style.transition = "all, linear, 1.5s";
      swapImg();
      clearInterval(timer);
    }
  });
});
