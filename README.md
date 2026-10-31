# Máy AI cá nhân StoryForge

[Mở notebook trong Colab](https://colab.research.google.com/github/Canhettg1133/storyforge-colab/blob/main/StoryForge-Personal-AI.ipynb)

Đây là mẫu công khai có sẵn mã và biểu mẫu cho **Máy AI cá nhân**. Backend hiện chỉ mở cho nhóm pilot được cho phép; đọc được mẫu không tự cấp quyền dùng StoryForge.

1. Đăng nhập StoryForge → **Cài đặt → Máy AI cá nhân → Kết nối máy AI → Mở Colab**.
2. Trong Colab chọn **Ghép nối / khởi động**, bấm **Chạy**.
3. Nhập mã vào StoryForge, kiểm tra đúng tài khoản và phiên máy rồi **Xác nhận liên kết**.
4. Chờ máy báo sẵn sàng → **Dùng máy này → Thử kết nối**. Giữ Colab hoạt động khi dùng AI.

Không cần xin quyền notebook Drive, tự chép mã, tạo Colab Secrets, nhập connector token hay tạo tài khoản Cloudflare. Không chia sẻ mã liên kết hoặc runtime.

## Mẫu và phiên riêng

Mở từ GitHub không tự lưu file vào Drive. **Tệp → Lưu bản sao vào Drive** là tùy chọn để giữ chỉnh sửa, không bắt buộc mỗi ngày. Người không có quyền ghi vào kho không sửa được nguồn GitHub; họ có thể chỉnh phiên/bản sao riêng.

Mỗi người dùng có runtime, liên kết, key và tunnel riêng. Mẫu không chứa output, lịch sử chạy, credential hoặc phiên của người khác. Credential phiên chỉ được nhận sau khi chủ tài khoản xác nhận mã hợp lệ trong StoryForge. Phiên runtime mới không mang theo model đã tải, RAM, tiến trình hay credential phiên cũ.

Colab không đảm bảo luôn có GPU, chạy 24/7 hoặc không ngắt. Tham khảo [FAQ Colab](https://research.google.com/colaboratory/faq.html) về tài nguyên và giới hạn dùng giao diện web ngoài notebook. Không đổi tài khoản để vượt hạn mức.

## Mặc định

| Mục | Giá trị |
| --- | --- |
| Model | GGUF khác |
| Repo | HauhauCS/Gemma-4-E4B-Uncensored-HauhauCS-Aggressive |
| File | Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q2_K_P.gguf |
| Context / max output | 64000 / 32000 |
| Thiết bị | Tự động |
| Model ID API | storyforge-local |

64000/32000 là giới hạn cấu hình, không phải bằng chứng đã inference đủ độ dài đó. Tốc độ và khả năng nạp model tùy bộ nhớ và runtime thực tế.

## Nguồn và cập nhật

Notebook được tạo bằng builder nhiều người dùng của StoryForge. ZIP/base64 trong ô mã chỉ để đóng gói mã Python và requirements, không phải mã hóa bí mật. `manifest.multiuser.json` ghi tên nguồn và SHA-256 của toàn bộ 9 tệp đóng gói, để đối chiếu với nguồn chuẩn trước phát hành.

Kho này chỉ phát hành notebook và manifest; không chứa dự án StoryForge riêng tư. Liên kết ở đầu README theo nhánh `main`; nút trong StoryForge được ghim commit đã kiểm tra. Khi cập nhật: sinh lại từ nguồn chuẩn, kiểm tra manifest/payload/output/bí mật và test, commit bộ ba tệp này, thử URL Colab ghim commit mới rồi cập nhật duy nhất `PERSONAL_AI_NOTEBOOK_URL` của backend pilot. Giữ URL phiên trước để rollback, không thay notebook cá nhân hoặc hostname cá nhân.
