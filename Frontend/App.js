// Backend API URL
        const API_URL = 'http://localhost:8000';

        let currentUser = {
            id: null,
            name: '',
            email: '',
            phone: '14002 54002',
            bio: 'Love helping my community and my peoples with various tasks!',
            credits: 25,
            rating: 4.8,
            servicesOffered: 0,
            servicesUsed: 8
        };

        let isLoggedIn = false;
        let authToken = null; // JWT token
        let currentServiceForBooking = null;
        let allUsers = [];
        let services = [];

        // Helper function to get auth headers
        function getAuthHeaders() {
            return {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            };
        }

        // Initialize App
        async function initApp() {
            // Check for saved token
            const savedToken = localStorage.getItem('authToken');
            const savedUser = localStorage.getItem('user');
            
            if (savedToken && savedUser) {
                authToken = savedToken;
                const user = JSON.parse(savedUser);
                currentUser.id = user.id;
                currentUser.name = user.name;
                currentUser.email = user.email;
                isLoggedIn = true;
                
                showSection('home');
                await loadUsers();
                await loadServices();
                updateUserStats();
            } else {
                showSection('auth');
            }
        }

        // API Functions
        async function loadUsers() {
            try {
                const response = await fetch(`${API_URL}/users`);
                const data = await response.json();
                if (data.success) {
                    allUsers = data.users;
                    console.log('Users loaded:', allUsers.length);
                }
            } catch (error) {
                console.error('Error loading users:', error);
                alert('Failed to load users. Make sure the backend is running!');
            }
        }

        async function loadSkillsFromBackend() {
            try {
                const response = await fetch(`${API_URL}/skills`);
                const data = await response.json();
                if (data.success) {
                    // Convert backend skills to frontend format
                    services = data.skills.map(skill => ({
                        id: skill.id,
                        title: skill.skill,
                        provider: skill.user_name || 'Unknown',
                        category: 'tech', // Default category
                        description: skill.description || 'No description',
                        rate: 1,
                        rating: 4.5,
                        reviews: 0,
                        user_id: skill.user_id
                    }));
                    console.log('Skills loaded:', services.length);
                }
            } catch (error) {
                console.error('Error loading skills:', error);
            }
        }

        // Section Navigation
        function showSection(sectionId) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Show selected section
            document.getElementById(sectionId).classList.add('active');
            
            // Load section-specific content
            if (sectionId === 'services') {
                loadServices();
            } else if (sectionId === 'profile') {
                loadUserProfile();
            }
        }

        // Authentication Functions
        async function login(event) {
            event.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            // Basic validation
            if (!validateEmail(email)) {
                showError('loginEmailError', 'Please enter a valid email');
                return;
            }
            
            if (password.length < 6) {
                showError('loginPasswordError', 'Password must be at least 6 characters');
                return;
            }
            
            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Store token and user info
                    authToken = data.access_token;
                    currentUser.id = data.user.id;
                    currentUser.name = data.user.name;
                    currentUser.email = data.user.email;
                    isLoggedIn = true;
                    
                    // Store token in localStorage
                    localStorage.setItem('authToken', authToken);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    
                    showSection('home');
                    await loadServices();
                    alert(`Welcome back, ${data.user.name}!`);
                } else {
                    showError('loginEmailError', data.detail || 'Login failed');
                }
            } catch (error) {
                console.error('Login error:', error);
                showError('loginEmailError', 'Login failed. Make sure the backend is running!');
            }
        }

        async function register(event) {
            event.preventDefault();
            
            const name = document.getElementById('regName').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;
            
            // Validation
            if (name.length < 2) {
                showError('regNameError', 'Name must be at least 2 characters');
                return;
            }
            
            if (!validateEmail(email)) {
                showError('regEmailError', 'Please enter a valid email');
                return;
            }
            
            if (password.length < 6) {
                showError('regPasswordError', 'Password must be at least 6 characters');
                return;
            }
            
            try {
                const response = await fetch(`${API_URL}/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: name,
                        email: email,
                        password: password
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Store token and user info
                    authToken = data.access_token;
                    currentUser.id = data.user.id;
                    currentUser.name = data.user.name;
                    currentUser.email = data.user.email;
                    currentUser.credits = 10; // Starting credits
                    isLoggedIn = true;
                    
                    // Store token in localStorage
                    localStorage.setItem('authToken', authToken);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    
                    showSection('home');
                    await loadServices();
                    alert(`Welcome to HelpX, ${name}!`);
                } else {
                    showError('regEmailError', data.detail || 'Registration failed');
                }
            } catch (error) {
                console.error('Registration error:', error);
                showError('regEmailError', 'Registration failed. Make sure the backend is running!');
            }
        }

        function logout() {
            isLoggedIn = false;
            authToken = null;
            currentUser = {
                id: null,
                name: '',
                email: '',
                phone: '14002 54002',
                bio: '',
                credits: 25,
                rating: 4.8,
                servicesOffered: 0,
                servicesUsed: 8
            };
            
            // Clear localStorage
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
            
            showSection('auth');
            alert('You have been logged out');
        }

        function showRegistration() {
            document.getElementById('loginForm').classList.add('hidden');
            document.getElementById('registrationForm').classList.remove('hidden');
        }

        function showLogin() {
            document.getElementById('registrationForm').classList.add('hidden');
            document.getElementById('loginForm').classList.remove('hidden');
        }

        // Validation Functions
        function validateEmail(email) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        }

        function showError(elementId, message) {
            document.getElementById(elementId).textContent = message;
            setTimeout(() => {
                document.getElementById(elementId).textContent = '';
            }, 5000);
        }

        // Services Functions
        async function loadServices() {
            await loadSkillsFromBackend();
            const grid = document.getElementById('servicesGrid');
            grid.innerHTML = '';
            
            if (services.length === 0) {
                grid.innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No services available yet. Be the first to post a service!</p>';
                return;
            }
            
            services.forEach(service => {
                const serviceCard = createServiceCard(service);
                grid.appendChild(serviceCard);
            });
        }

        function createServiceCard(service) {
            const card = document.createElement('div');
            card.className = 'service-card';
            card.innerHTML = `
                <div class="service-header">
                    <div class="service-title">${service.title}</div>
                    <div class="service-provider">by ${service.provider}</div>
                    <span class="service-category">${getCategoryName(service.category)}</span>
                </div>
                <div class="service-body">
                    <p class="service-description">${service.description}</p>
                </div>
                <div class="service-footer">
                    <div class="time-rate">${service.rate} credit${service.rate > 1 ? 's' : ''}/hour</div>
                    <div class="rating">
                        ${'★'.repeat(Math.floor(service.rating))} ${service.rating} (${service.reviews})
                    </div>
                </div>
                <div style="padding: 1rem;">
                    <button class="btn btn-primary" style="width: 100%;" onclick="openBookingModal(${service.id})">
                        Book Service
                    </button>
                </div>
            `;
            return card;
        }

        function getCategoryName(category) {
            const categories = {
                'home': 'Home & Garden',
                'tech': 'Technology',
                'education': 'Education',
                'health': 'Health & Wellness',
                'creative': 'Creative',
                'transport': 'Transport'
            };
            return categories[category] || category;
        }

        function filterServices() {
            const searchTerm = document.getElementById('serviceSearch').value.toLowerCase();
            const categoryFilter = document.getElementById('categoryFilter').value;
            
            let filteredServices = services.filter(service => {
                const matchesSearch = service.title.toLowerCase().includes(searchTerm) ||
                                    service.description.toLowerCase().includes(searchTerm) ||
                                    service.provider.toLowerCase().includes(searchTerm);
                
                const matchesCategory = !categoryFilter || service.category === categoryFilter;
                
                return matchesSearch && matchesCategory;
            });
            
            const grid = document.getElementById('servicesGrid');
            grid.innerHTML = '';
            
            filteredServices.forEach(service => {
                const serviceCard = createServiceCard(service);
                grid.appendChild(serviceCard);
            });
        }

        async function postService(event) {
            event.preventDefault();
            
            if (!currentUser.id || !authToken) {
                alert('Please login first to post a service!');
                return;
            }
            
            const title = document.getElementById('serviceTitle').value;
            const category = document.getElementById('serviceCategory').value;
            const description = document.getElementById('serviceDescription').value;
            const rate = parseInt(document.getElementById('serviceRate').value);
            
            try {
                const response = await fetch(`${API_URL}/add-skill?skill=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}`, {
                    method: 'POST',
                    headers: getAuthHeaders()
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    alert('Service posted successfully!');
                    await loadServices();
                    currentUser.servicesOffered++;
                    updateUserStats();
                    closeModal('postServiceModal');
                    
                    // Clear form
                    document.getElementById('serviceTitle').value = '';
                    document.getElementById('serviceCategory').value = '';
                    document.getElementById('serviceDescription').value = '';
                    document.getElementById('serviceRate').value = '1';
                } else {
                    if (response.status === 401) {
                        alert('Your session has expired. Please login again.');
                        logout();
                    } else {
                        alert('Failed to post service: ' + (data.detail || 'Unknown error'));
                    }
                }
            } catch (error) {
                console.error('Error posting service:', error);
                alert('Failed to post service. Make sure the backend is running!');
            }
        }

        // Profile Functions
        async function loadUserProfile() {
            document.getElementById('userName').textContent = currentUser.name || 'Guest';
            document.getElementById('userEmail').textContent = currentUser.email || 'Not logged in';
            
            if (currentUser.name) {
                document.getElementById('userAvatar').textContent = currentUser.name.split(' ').map(n => n[0]).join('');
            }
            
            // Count user's services
            if (currentUser.id) {
                try {
                    const response = await fetch(`${API_URL}/skills?user_id=${currentUser.id}`);
                    const data = await response.json();
                    if (data.success) {
                        currentUser.servicesOffered = data.count;
                    }
                } catch (error) {
                    console.error('Error loading user services:', error);
                }
            }
            
            updateUserStats();
        }

        function updateUserStats() {
            document.getElementById('totalCredits').textContent = currentUser.credits;
            document.getElementById('servicesOffered').textContent = currentUser.servicesOffered;
            document.getElementById('servicesUsed').textContent = currentUser.servicesUsed;
            document.getElementById('userRating').textContent = currentUser.rating;
            document.getElementById('userCredits').textContent = `${currentUser.credits} Credits`;
        }

        function updateProfile(event) {
            event.preventDefault();
            
            currentUser.name = document.getElementById('editName').value;
            currentUser.email = document.getElementById('editEmail').value;
            currentUser.phone = document.getElementById('editPhone').value;
            currentUser.bio = document.getElementById('editBio').value;
            
            loadUserProfile();
            closeModal('editProfileModal');
        }

        // Booking Functions
        function openBookingModal(serviceId) {
            currentServiceForBooking = services.find(s => s.id === serviceId);
            openModal('bookServiceModal');
        }

        function bookService(event) {
            event.preventDefault();
            
            const date = document.getElementById('bookingDate').value;
            const time = document.getElementById('bookingTime').value;
            const duration = parseInt(document.getElementById('bookingDuration').value);
            const notes = document.getElementById('bookingNotes').value;
            
            // Simulate booking process
            alert(`Booking request sent to ${currentServiceForBooking.provider} for ${date} at ${time} (${duration} hour${duration > 1 ? 's' : ''})`);
            
            closeModal('bookServiceModal');
            
            // Clear form
            document.getElementById('bookingDate').value = '';
            document.getElementById('bookingTime').value = '';
            document.getElementById('bookingDuration').value = '1';
            document.getElementById('bookingNotes').value = '';
        }

        // Messages Functions
        function selectContact(element, contactName) {
            // Remove active class from all contacts
            document.querySelectorAll('.contact').forEach(contact => {
                contact.classList.remove('active');
            });
            
            // Add active class to selected contact
            element.classList.add('active');
            
            // Update chat header
            document.getElementById('chatHeader').textContent = contactName;
            
            // Load messages for this contact (simplified for demo)
            loadMessages(contactName);
        }

        function loadMessages(contactName) {
            const chatMessages = document.getElementById('chatMessages');
            
            // Sample messages based on contact
            const messages = {
                'Levi Ackerman': [
                    { type: 'received', content: 'Hi! I saw your gardening service. Could you help me with my vegetable garden this weekend?' },
                    { type: 'sent', content: 'Absolutely! I\'d be happy to help. What time works best for you?' },
                    { type: 'received', content: 'Saturday morning around 9 AM would be perfect. Thanks for the gardening help!' }
                ],
                'Mukesh': [
                    { type: 'received', content: 'Hi! I need help with Excel formulas. When can we schedule the tutoring?' },
                    { type: 'sent', content: 'I can help you this week. How about Wednesday evening?' },
                    { type: 'received', content: 'Perfect! See you Wednesday at 7 PM.' }
                ],
                'Dr.Prem': [
                    { type: 'sent', content: 'Thanks for the wonderful photography session today!' },
                    { type: 'received', content: 'You\'re very welcome! The photos turned out great.' },
                    { type: 'sent', content: 'I\'ll definitely recommend you to my friends!' }
                ]
            };
            
            const contactMessages = messages[contactName] || [];
            
            chatMessages.innerHTML = '';
            contactMessages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${msg.type}`;
                messageDiv.innerHTML = `<div class="message-content">${msg.content}</div>`;
                chatMessages.appendChild(messageDiv);
            });
            
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function sendMessage() {
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            
            if (!message) return;
            
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message sent';
            messageDiv.innerHTML = `<div class="message-content">${message}</div>`;
            chatMessages.appendChild(messageDiv);
            
            messageInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function handleMessageKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Modal Functions
        function openModal(modalId) {
            document.getElementById(modalId).classList.add('active');
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.classList.remove('active');
            }
        }

        // Initialize app when page loads
        document.addEventListener('DOMContentLoaded', function() {
            initApp();
            
            // Set minimum date for booking to today
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('bookingDate').setAttribute('min', today);
        });