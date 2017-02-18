var takePicture = document.getElementById("take-picture");

var canvas = document.createElement("canvas");
var codeType = document.getElementById("code-type");
var codeContent = document.getElementById("code-content");
var pathFound='search/?criteria=scnr';

var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.itemMediaForm').on('submit', function(event){
    event.preventDefault();
    var $form = $(this);

    var fields = $form.serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});

    $.ajax({
        url: "/rate/",
        type: "POST",
        data: {"item_id": fields["item_id"], "bin_name": fields["bin_name"]},
        dataType: "json",
        success: function (result) {
            $form.find("span.rating").text(result["total_rating"]);
            if ($form.find("a.rateButton").hasClass("voteThumb")) {
                $form.find("a.rateButton").removeClass("voteThumb");
            }
            else  {
                $form.find("a.rateButton").addClass("voteThumb");
            }
        }
    });
});

function scan() {
  if (typeof MozActivity !== 'undefined') {
    // in Firefox OS v1.0.1, input[file] does not work, using Web Activities
    takePictureUsingWebActivity();
    return;
  }

  takePicture.click();
}

function takePictureUsingWebActivity() {
  var pick = new MozActivity({
    name: "pick",
    data: { type: ["image/png", "image/jpg", "image/jpeg"] }
  });
  pick.onsuccess = function () {
    loadImage(URL.createObjectURL(this.result.blob));
  };
}

takePicture.onchange = function (event) {
  var files = event.target.files;
  if (!files || files.length === 0) {
    return;
  }

  var file = files[0];
  var imgURL = (window.URL || window.webkitURL).createObjectURL(file);
  loadImage(imgURL);
}

function loadImage(imgURL) {
    // process the user taken picture
  // clean
  codeType.textContent = '';
  codeContent.value = '';


  var img = new Image();
  img.onload = function () {
    var canvas = document.createElement('canvas');
    // resizing image to 320x240 for slow devices
    var k = (320 + 240) / (img.width + img.height);
    canvas.width = Math.ceil(img.width * k);
    canvas.height = Math.ceil(img.height * k);
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, img.width, img.height,
                  0, 0, canvas.width, canvas.height);

    var data = ctx.getImageData(0, 0, canvas.width, canvas.height);

    var t0 = Date.now();
    var codes = cakeProcessImageData(data);
    var t = Date.now() - t0;
    document.body.classList.remove('processing');

      if (codes.length === 0) {
          codeType.textContent = 'N/A';
          window.location.href = 'search/?criteria=NOTFOUND'
          document.body.classList.add('not-detected');
          return;
      }

      var type = codes[0][0];
      var data = codes[0][2];
      // publishing data
      codeType.textContent = type;
      codeContent.value = data;
      window.location.href = pathFound + codeContent.value;
  };

  img.src = imgURL;

}
