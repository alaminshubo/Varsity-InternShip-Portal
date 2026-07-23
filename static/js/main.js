// পেজটি পুরোপুরি লোড হওয়ার পর কোডটি সচল হবে
document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.getElementById('role');
    const studentIdGroup = document.getElementById('student-id-group');
    const departmentGroup = document.getElementById('department-group');
    const studentIdInput = document.getElementById('student_id');
    const departmentInput = document.getElementById('department');

    // যদি এলিমেন্টগুলো পেজে খুঁজে পাওয়া যায়, তবেই লজিক কাজ করবে
    if (roleSelect && studentIdGroup && departmentGroup) {
        function toggleFields() {
            if (roleSelect.value === 'company') {
                // কোম্পানি সিলেক্ট করলে হাইড হবে
                studentIdGroup.style.display = 'none';
                departmentGroup.style.display = 'none';
                
                // HTML validation বন্ধ করার জন্য required সরিয়ে দেওয়া হলো
                studentIdInput.required = false;
                departmentInput.required = false;
            } else {
                // স্টুডেন্ট সিলেক্ট করলে আবার শো করবে
                studentIdGroup.style.display = 'block';
                departmentGroup.style.display = 'block';
                
                // স্টুডেন্টের জন্য আবার বাধ্যতামূলক করা হলো
                studentIdInput.required = true;
                departmentInput.required = true;
            }
        }

        // ইউজার ড্রপডাউন চেঞ্জ করলে ফাংশনটি রান করবে
        roleSelect.addEventListener('change', toggleFields);
        
        // পেজ প্রথমবার ওপেন হওয়ার সময় একবার রান করবে চ্যাকিংয়ের জন্য
        toggleFields();
    }
});