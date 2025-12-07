/*产品目录 begin*/
/*产品目录第一个默认展开*/
//$(function(){ $(".cp_type .bd ul li").first().children('div').show();$(".cp_type .bd ul li").first().addClass('on');});

$(".cp_type .bd ul li p span").click(function () {
	if($(this).parents('li').hasClass('on')){
		$(this).parents('li').removeClass('on').find('div').stop().slideUp();
	}else{
		$(this).parents('li').find('div').removeAttr("style");
		$(this).parents('li').addClass('on').find('div').stop().slideDown();
	}
});
if(document.body.clientWidth <= 1079){  
	$(".cp_type .hd").click(function () {
		if($(this).hasClass('on')){
			$(this).next('div').removeAttr("style");
			$(this).removeClass('on').next('div').stop().slideUp();
		}else{
			$(this).next('div').removeAttr("style");
			$(this).addClass('on').next('div').stop().slideDown();
		}
	});
}
/*产品目录 end*/
		
//手机端导航
$(function () {
		$(".menu_open").click(function () {
			$(".nav").animate({ 'left': '0' }, 400);
			$(".hcover").animate({ 'right': '0' }, 400);
		});
		$(".hcover").click(function () {
			$(this).animate({ 'right': '-50%' }, 400);
			$(".nav").animate({ 'left': '-50%' }, 400);
			$(".nav_ul").animate({ 'left': '0' }, 400);
			$('.nav_item_open').css('left', '-50%');
		});
		$(".nav_item i").click(function () {
			$(".nav_ul").animate({ 'left': '-100%' }, 400);
			$(this).next('.nav_item_open').css('left', '0');
		});
		$(".subopen").click(function () {
			$(this).parent('.nav_item_open').css('left', '-50%');
			$(".nav_ul").animate({ 'left': '0' }, 400);
		});
	});

 

//banenr切换
var swiper1 = new Swiper('.apple-banner .swiper-container', {      
        autoplay: 3000,//自动播放时间
        loop: true,//开启循环true or false
        slidesPerView: 1, //列数
        spaceBetween: 0, //slides之间间隔
        breakpointsInverse: true,
        nextButton: '.apple-banner .swiper-button-next',
        prevButton: '.apple-banner .swiper-button-prev',
        pagination: '.apple-banner .swiper-pagination',
		observer:true,
        observeParents:true,
        autoplayDisableOnInteraction:false,
		paginationClickable: true,
        breakpoints: {
            320: {
                slidesPerView: 1,
                spaceBetween: 0
            },
            767: {
                slidesPerView: 1,
                spaceBetween: 0
            },
            1080: {
                slidesPerView: 1,
                spaceBetween: 0
            },
            1200: {
                slidesPerView: 1,
                spaceBetween: 0
            }
        }
    });
	

//首页推荐产品
	var swiper2 = new Swiper('.indtjpro .swiper-container2', {		
		autoplay: 3000,//自动播放时间
		loop: true,//开启循环true or false
		slidesPerView:4,//列数
		spaceBetween:26,//slides之间间隔
		breakpointsInverse: true,
		nextButton: '.indtjpro .swiper-button-next',
		prevButton: '.indtjpro .swiper-button-prev',
		paginationClickable: true,
            observer:true,
            observeParents:true,
            autoplayDisableOnInteraction:false,
		breakpoints: {
			550: {
				slidesPerView: 2,
				spaceBetween: 10
			},
			767: {
				slidesPerView:2,
				spaceBetween: 20
			},
			1079: {
				slidesPerView:3,
				spaceBetween:26
			},
		}
	});

//首页技术文章
	var swiper2 = new Swiper('.ind_article .swiper-container3', {		
		autoplay: 3000,//自动播放时间
		loop: true,//开启循环true or false
		slidesPerView:3,//列数
		spaceBetween:30,//slides之间间隔
		breakpointsInverse: true,
		nextButton: '.ind_article .swiper-button-next',
		prevButton: '.ind_article .swiper-button-prev',
		paginationClickable: true,
            observer:true,
            observeParents:true,
            autoplayDisableOnInteraction:false,
		breakpoints: {
			500: {
				slidesPerView: 1,
				spaceBetween: 0
			},
			767: {
				slidesPerView:2,
				spaceBetween: 20
			},
			1079: {
				slidesPerView:2,
				spaceBetween:26
			},
		}
	});
		
