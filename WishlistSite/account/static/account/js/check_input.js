$(document).ready(function() {
      var usernameInput = $('#id_username');
      var emailInput = $('#id_email');
      var form = $('#registration-form');

      usernameInput.on('input', function() {
        var username = usernameInput.val();
        $.ajax({
          url: '/account/check-username-email/',
          type: 'GET',
          data: { username: username },
          success: function(response) {
            var usernameError = $('#username-error');
            if (response.result == true) {
              usernameError.text('Пользователь с таким логином уже существует');
              usernameInput.attr('class', 'form-control error');
            } else {
              usernameError.text('');
              usernameInput.attr('class', 'form-control');
            }
          }
        });
      });

      emailInput.on('input', function() {
        var email = emailInput.val();
        $.ajax({
          url: '/account/check-username-email/',
          type: 'GET',
          data: { email: email },
          success: function(response) {
            var emailError = $('#email-error');
            if (response.result == true) {
              emailError.text('Пользователь с такой почтой уже существует');
              emailInput.attr('class', 'form-control error');
            } else {
              emailError.text('');
              emailInput.attr('class', 'form-control');
            }
          }
        });
      });
    });