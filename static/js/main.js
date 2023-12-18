 //validating start and end date
 function validateForm() {
         let start = document.forms["tempform"]["from"].value;
         let end= document.forms["tempform"]["to"].value;
          if (start == "" && start < "2023-05-1") {
              alert("start date must be filled out and not less than 2023-05-1");
             return false;
              }
            if (end== "") {
              alert("end date must be filled out");
              return false;
              }
            }
//change the color of the textbox when user entered data
 function changeBackgroundColor(textbox) {
      // Check if the textbox has text
      if (textbox.value.trim() !== "") {
        // Change the background color when there is text
        textbox.style.backgroundColor = '#ff4500';
      } else {
        // Reset the background color when there is no text
        textbox.style.backgroundColor = '';
      }
    }