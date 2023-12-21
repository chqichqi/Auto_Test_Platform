(function($) {
    jQuery(document).ready(function() {
        var $modalContainer = jQuery('<div class="modal-container"><div class="inner-div">' +
            '正在测试已用时>><span id="test-time">0</span>秒，请耐心等待...</div></div>');
        var $actionButton = jQuery('button[eid="3"][data-name="run_case"]');   //获得自定义的开始测试按钮
        var $checkboxes = jQuery('input.action-select');   // 获得页面上的复选框对象
        // 获取弹出提示框中的确定按钮，好像获取失败了
        // var $confirmButton = jQuery('.action-confirmation button[type="submit"]');
        // var buttonElement = document.querySelector('.el-button.el-button--default.el-button--small.el-button--primary');
        var timerElement = document.getElementById('timer');
        var startTime; // 获取当前时间（单位：秒）

        console.log('Executing JavaScript...');

        function showModal() {
            // Set display to 'block' before appending to the body
            $modalContainer.css('display', 'block');
            jQuery('body').append($modalContainer);
            // setTimeout(() => console.log('延时1秒'), 1000);    // 延时200毫秒
            updateTimer();
            setInterval(updateTimer, 1000); // 更新时间间隔为1秒
            console.log('Executing showModal');
        }

        function updateTimer() {
            var currentTime = new Date().getTime() / 1000;
            var elapsedTime = Math.round(currentTime - startTime);
            jQuery('#test-time').text(formatTime(elapsedTime));
        }

        function formatTime(seconds) {
            var hour = Math.floor(seconds / 3600);
            var minutes = Math.floor(seconds / 60);
            var remainingSeconds = seconds % 60;
            if(hour>0){
                return hour + '时' + minutes + '分' + remainingSeconds;
            }else if (minutes>0){
                return minutes + '分' + remainingSeconds;
            }else{
                return remainingSeconds;
            }

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

        // 直接验证是否点击开始测试按钮
        $actionButton.on('click', function() {
            // 通过判断页面上是否勾选了记录来决定是否显示showModal();
            console.log('record count='+console.log($checkboxes.length));
            console.log('selected record number='+$checkboxes.filter(':checked').length);
            // setTimeout(() => console.log('延时1'), 100);    // 延时200毫秒
            // setInterval(function(){alert('延时2')}, 20);    // 延时200毫秒
            if ($checkboxes.filter(':checked').length === 0) {
                console.log('no selected record：not showModal');
                return;
            }
            startTime = new Date().getTime() / 1000; // 获取当前时间（单位：秒）
            showModal();
        });
    });
})(django.jQuery);
