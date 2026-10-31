# Máy AI cá nhân StoryForge

[Mở mẫu Colab](https://colab.research.google.com/github/Canhettg1133/storyforge-colab/blob/main/StoryForge-Personal-AI.ipynb)

Mẫu công khai chỉ chứa notebook, manifest và hướng dẫn. Backend vẫn chỉ mở cho nhóm pilot được cho phép.
Quyền đọc mẫu không cấp quyền dùng StoryForge và không cấp quyền sửa nguồn GitHub.
Nút Mở Colab trong StoryForge được operator ghim vào commit đã kiểm tra.

Cập nhật01/11: sửa kiểm tra giới hạn đầu ra của llama.cpp b11981. Khi `/props` báo
`n_predict=-1`, notebook đối chiếu lệnh tiến trình thật thay vì kết luận nhầm cấu hình sai.
Vẫn kiểm file/context, giới hạn gateway và đầy đủ model/API/HTTPS trước khi báo sẵn sàng.

1. Đăng nhập StoryForge → Cài đặt → Máy AI cá nhân → Kết nối máy AI → Mở Colab.
2. Chọn Ghép nối / khởi động, bấm Chạy và nhập mã notebook hiện ra vào StoryForge.
3. Đọc đúng tài khoản và phiên notebook, bấm **Liên kết và dùng máy này**.
4. Chờ máy sẵn sàng. Giao diện mới tự chọn đúng máy vừa liên kết khi không có lượt sinh hoặc Auto Write.
5. **Thử kết nối** là thao tác chủ động để kiểm tra Direct; heartbeat/ready không thay thế phép thử đó.
   Nếu tự chọn thất bại, bấm **Dùng máy này** để thử lại. Giao diện cũ vẫn cần Xác nhận rồi Dùng máy này;
   notebook không tự nâng cấp website.

Không cần xin quyền Drive, Colab Secrets, chép key hoặc tự cấu hình tunnel. Lưu bản sao vào Drive là tùy chọn.
Mỗi người cần runtime và liên kết riêng. Không chia sẻ mã, output hoặc runtime.
Phiên mới không kế thừa RAM, model đã nạp hoặc credential của phiên trước.

| Mục | Mặc định |
| --- | --- |
| Model | GGUF khác |
| Repo | HauhauCS/Gemma-4-E4B-Uncensored-HauhauCS-Aggressive |
| File | Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q8_K_P.gguf |
| Context tổng | 128000 |
| Đầu ra tối đa | 64000 |
| Thiết bị | Tự động |
| Model ID API | storyforge-local |

Context gồm đầu vào, lịch sử, hướng dẫn và đầu ra. 64000 là giới hạn, không bắt mọi câu trả lời sinh đủ số đó.
File Q8 khoảng 8,13 GB không chứng minh GPU đủ bộ nhớ. Chưa nghiệm thu nạp Q8/128000/64000 hoặc suy luận
đủ độ dài trên Colab thật. Không dùng câu thử ngắn để suy ra khả năng chạy gần giới hạn. Notebook không tự hạ cấu hình.

Chạy lại cùng cấu hình dùng lại máy đã kiểm tra. Cấu hình sai/tải lỗi hoặc model bận giữ máy cũ nếu còn hoạt động.
Đổi model dùng khóa chung với lượt sinh, dừng model cũ trước khi nạp model mới. Không đổi pairing/key/hostname/tunnel.
Notebook hiển thị tên GGUF và giới hạn đã kiểm tra qua llama.cpp, tách cấu hình yêu cầu chưa áp dụng.
Nếu nạp mới thất bại sau khi chuyển, chọn **Khôi phục cấu hình trước** để thử nạp lại; không bảo đảm khôi phục luôn thành công.
Khi nâng từ mã gateway cũ trong cùng kernel, cần chủ động dừng máy chủ trước khi chạy mã mới; không tự cắt lượt đang sinh.

Ready gửi sớm qua heartbeat đã xác thực sau kiểm tra model/gateway/tunnel. Heartbeat định kỳ 60 giây,
lease tối đa 120 giây, phiên tối đa 8 giờ. Lỗi đồng bộ có retry hữu hạn, không tạo credential mới.
Key/control/connector chỉ ở bộ nhớ runtime và môi trường tiến trình; file lease không chứa secret.
Thu hồi hoặc hết lease chặn gateway/stream. Runtime có thể sửa code nên ready vẫn chỉ là máy tự báo.

Notebook được sinh từ nguồn chuẩn, output rỗng, execution count null; manifest chứa SHA-256 của từng tệp payload.
ZIP/base64 chỉ đóng gói, không che giấu bí mật. Không sửa notebook cá nhân cũ hoặc hostname colab.storyforge.io.vn.
Colab không bảo đảm GPU/thời lượng phiên. Xem [FAQ Colab](https://research.google.com/colaboratory/faq.html).
