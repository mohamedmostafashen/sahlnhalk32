document.querySelectorAll('ul li a').forEach(item => {
    item.addEventListener('click', (e) => {
        if (item.textContent.includes('مغلق')) {
            e.preventDefault();
            alert('هذا المحتوى مغلق حتى النجاح في الاختبار السابق!');
        }
    });
});
