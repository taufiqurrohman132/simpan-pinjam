// Toggle Sidebar
document.getElementById("toggleBtn").addEventListener("click", function() {
  document.getElementById("sidebar").classList.toggle("collapsed");
});

// Toggle Dropdown Menu (admin ▼)
document.getElementById("userMenu").addEventListener("click", function() {
  document.getElementById("dropdownMenu").classList.toggle("show");
});

// Toggle Submenu Simpanan
const simpananMenu = document.querySelector('.sidebar ul li:nth-child(3)');
const simpananSub = simpananMenu.querySelector('ul');

simpananMenu.addEventListener('click', () => {
  simpananSub.style.display = simpananSub.style.display === 'block' ? 'none' : 'block';
});

// Waktu & Tanggal Otomatis
function updateDateTime() {
  const now = new Date();
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  const time = now.toLocaleTimeString('id-ID');
  const date = now.toLocaleDateString('id-ID', options);
  document.getElementById("datetimeText").innerText = `${date}, ${time}`;
}
setInterval(updateDateTime, 1000);
updateDateTime();

