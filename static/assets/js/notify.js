type = ['primary', 'info', 'success', 'warning', 'danger'];

demo = {
    showNotification: function(from, align, message) {
        color = Math.floor((Math.random() * 4) + 1);
    
        $.notify({
          icon: "tim-icons icon-check-2",
          message: message
    
        }, {
          type: type['success'],
          timer: 1500,
          placement: {
            from: from,
            align: align
          }
        });
    }
}