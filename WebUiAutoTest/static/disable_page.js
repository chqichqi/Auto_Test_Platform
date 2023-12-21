(function($) {
    $(document).ready(function() {
        // 禁用整个页面
        $('body').addClass('disabled-page');

        // 或者禁用所有元素
        $(':input').prop('disabled', true);
    });
})(django.jQuery);
