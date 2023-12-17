(function($) {
    jQuery(document).ready(function() {
        // // var $modalContainer = jQuery('<div class="modal-container"><div class="inner-div"><p>正在测试中，请耐心等待...</p></div></div>');
        // var $modalContainer = jQuery('<div class="modal-container"><div class="outer-div"><div class="inner-div">正在测试中，请耐心等待...</div></div></div>');
        var $modalContainer = jQuery('<div class="modal-container">正在测试中，请耐心等待...</div>');
        // var $modalOverlay = jQuery('<div class="modal-overlay"></div>');   // 另一个css
        var $actionButton = jQuery('button[eid="3"][data-name="run_case"]');
        var $checkboxes = jQuery('input.action-select');

        console.log('Executing JavaScript...');

        function showModal() {
            // Set display to 'block' before appending to the body
            $modalContainer.css('display', 'block');
            jQuery('body').append($modalContainer);
            console.log('Executing showModal');
        }

        function hideModal() {
            console.log('Executing remove');
            $modalContainer.remove();
        }

        function onLongRunningActionComplete() {
            hideModal();
            // Add other actions to perform after completion
            console.log('Executing hideModal');
        }

        $actionButton.on('click', function() {
            // 通过判断页面上是否勾选了记录来决定是否显示showModal();
            console.log('记录总数='+console.log($checkboxes.length));
            console.log('已勾选的记录数='+$checkboxes.filter(':checked').length);
            // setTimeout(() => console.log('延时1'), 100);    // 延时200毫秒
            // setInterval(function(){alert('延时2')}, 20);    // 延时200毫秒
            if ($checkboxes.filter(':checked').length === 0) {
                console.log('未勾选记录则退出不显示：showModal');
                return;
            }
            showModal();
        });

        // Include CSRF token in the request headers
        // var csrfToken = jQuery('[name=csrfmiddlewaretoken]').val();

        // Simulate a long-running action with an Ajax request
        // jQuery.ajax({
        //     type: 'POST',
        //     url: '{% url "/WebUiAtuoTest/templates/admin/base_site.html" %}', // Replace with your actual view URL
        //     headers: {
        //         'X-CSRFToken': csrfToken
        //     },
        //     success: function(response) {
        //         onLongRunningActionComplete();
        //     },
        //     error: function(error) {
        //         // Handle error
        //         console.error('Ajax request error:', error);
        //     }
        // });
    });
})(django.jQuery);
