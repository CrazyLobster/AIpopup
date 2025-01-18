// 示例图片数据
const sampleImages = [
    {
        url: 'https://images.pexels.com/photos/1779487/pexels-photo-1779487.jpeg',
        title: '现代工作区设置',
        author: 'John Doe'
    },
    {
        url: 'https://images.pexels.com/photos/1714208/pexels-photo-1714208.jpeg',
        title: '紫色氛围的工作站',
        author: 'Jane Smith'
    },
    {
        url: 'https://images.pexels.com/photos/1279107/pexels-photo-1279107.jpeg',
        title: '笔记本电脑工作区',
        author: 'Mike Johnson'
    }
    // 可以添加更多图片
];

// 初始化页面
document.addEventListener('DOMContentLoaded', () => {
    loadImages();
    setupSearch();
    setupFilters();
});

// 加载图片到网格中
function loadImages(images = sampleImages) {
    const imageGrid = document.querySelector('.image-grid');
    imageGrid.innerHTML = ''; // 清空现有内容

    images.forEach(image => {
        const card = createImageCard(image);
        imageGrid.appendChild(card);
    });
}

// 创建图片卡片元素
function createImageCard(image) {
    const card = document.createElement('div');
    card.className = 'image-card';
    
    card.innerHTML = `
        <img src="${image.url}" alt="${image.title}">
        <div class="image-info">
            <h3>${image.title}</h3>
            <p>by ${image.author}</p>
        </div>
    `;

    // 添加点击事件
    card.addEventListener('click', () => {
        // 可以在这里添加点击图片后的行为，比如打开大图
        console.log('Clicked image:', image.title);
    });

    return card;
}

// 设置搜索功能
function setupSearch() {
    const searchInput = document.querySelector('.search-container input');
    const searchBtn = document.querySelector('.search-btn');

    const handleSearch = () => {
        const searchTerm = searchInput.value.toLowerCase();
        const filteredImages = sampleImages.filter(image => 
            image.title.toLowerCase().includes(searchTerm) ||
            image.author.toLowerCase().includes(searchTerm)
        );
        loadImages(filteredImages);
    };

    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
}

// 设置筛选功能
function setupFilters() {
    const sortSelect = document.querySelector('.sort-select');
    
    sortSelect.addEventListener('change', () => {
        const sortValue = sortSelect.value;
        let sortedImages = [...sampleImages];

        switch(sortValue) {
            case '最新':
                // 这里可以添加实际的排序逻辑
                sortedImages.reverse();
                break;
            case '最热':
                // 随机排序作为示例
                sortedImages.sort(() => Math.random() - 0.5);
                break;
            case '推荐':
                // 这里可以添加推荐算法
                break;
            default:
                // 默认排序
                break;
        }

        loadImages(sortedImages);
    });
}

// 添加滚动加载更多功能
window.addEventListener('scroll', () => {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1000) {
        // 这里可以添加加载更多图片的逻辑
        console.log('Loading more images...');
    }
}); 