$(document).ready(function() {
    $('#startDetectionButton').click(function() {
        $.ajax({
            url: '/start_detection',
            type: 'GET',
            beforeSend: function() {
                $('#startDetectionButton').prop('disabled', true); // Disable button during detection
            },
            success: function(response) {
                console.log(response);
                $('#detectionStatus').text(response.message); // Display detection status
            },
            error: function(error) {
                console.log(error);
                $('#detectionStatus').text('Error occurred during detection.');
            },
            complete: function() {
                $('#startDetectionButton').prop('disabled', false); // Re-enable button after detection
            }
        });
    });

    $('#stopDetectionButton').click(function() {
        $.ajax({
            url: '/stop_detection',
            type: 'GET',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
