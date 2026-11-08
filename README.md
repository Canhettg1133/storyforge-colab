# Máy AI cá nhân StoryForge · Q/IQ và nhiều yêu cầu văn bản

## Cập nhật 08/11/2026: xử lý tải file bị kẹt hoặc lỗi HTTP

- Sau khi cài thư viện, notebook hiển thị riêng bước tải công cụ GPU/CPU từ GitHub. Khi lỗi, thông báo có tên file và mã HTTP; một số lỗi mạng tạm thời được thử tối đa ba lần. File tải dở không được coi là công cụ đã tải xong.
- GGUF công khai được tải trong tiến trình riêng. Bấm Dừng sẽ dừng cả tiến trình tải và giải phóng khóa; trên Linux, lượt tải cũng thoát nếu tiến trình notebook bị dừng đột ngột.
- Chờ khóa GGUF tối đa 60 giây, tổng thời gian một lượt tải tối đa 30 phút, có thông báo chờ mỗi 30 giây. Không tự xóa khóa/cache hoặc thay cấu hình model.
- Nếu đã bị kẹt bằng bản cũ, khởi động lại phiên Colab bằng **Runtime → Restart session**, rồi mở mẫu mới và ghép nối lại. Tải lại trang hoặc kết nối lại đơn thuần không bảo đảm dừng lượt tải cũ. Khởi động lại phiên sẽ dừng máy AI hiện tại và mất quyền phiên trong bộ nhớ; cache còn hay không phụ thuộc máy ảo Colab.

Đã qua **158 kiểm thử trên Linux**, bao gồm khóa file thật, dừng tiến trình, thoát theo phiên notebook và thư viện Hugging Face với máy chủ tải thử cục bộ. Chưa thử tải model nhiều GB hoặc inference GPU Colab thật cho bản sửa này.

Mẫu Colab công khai, không cần chép code hoặc nhập key. Mở **StoryForge → Cài đặt → Máy AI cá nhân → Mở Colab** để nhận URL ghim đúng phiên bản. Mở mẫu chưa tự tải model. Có thể lưu bản sao vào Drive nếu muốn giữ chỉnh sửa; mỗi người cần runtime và liên kết riêng.

Trong biểu mẫu, chọn model, thiết bị và **số yêu cầu đồng thời: 1, 3 hoặc 5**. Sau đó chủ động chạy **Ghép nối / khởi động**, nhập mã vào StoryForge và xác nhận theo luồng hiện có. Không chia sẻ runtime hoặc output phiên liên kết.

Mặc định: **Q8_K_P**, **128000 context mỗi yêu cầu**, **64000 output tối đa**, **Tự động**, API model **storyforge-local**, **3 slot**. Không tự giảm model, token hoặc slot khi thiếu bộ nhớ. **5 slot là cấu hình thử nghiệm**, chưa được benchmark trên GPU thật.

## Danh sách đã xác minh ngày 02/11/2026

Nguồn: [Hugging Face](https://huggingface.co/HauhauCS/Gemma-4-E4B-Uncensored-HauhauCS-Aggressive/tree/45b6a334b4bcd1d7f37179df58b3b1d66a184e5d).
Tất cả lựa chọn Q/IQ ghim revision `45b6a334b4bcd1d7f37179df58b3b1d66a184e5d`; tên file chính xác và dung lượng được đóng gói trong `model_catalog.json` bên trong notebook. Không có mmproj trong danh sách sinh văn bản. Chọn **GGUF khác** để nhập repo, file và revision riêng; ba trường này chỉ áp dụng cho lựa chọn đó.

| Bản | Dung lượng file (GB thập phân) |
| --- | ---: |
| Q2_K_P | 4.432 |
| IQ3_M | 4.715 |
| Q3_K_M | 4.850 |
| Q3_K_P | 4.885 |
| IQ4_XS | 5.071 |
| Q4_K_M | 5.335 |
| Q4_K_P | 5.369 |
| Q5_K_M | 5.763 |
| Q5_K_P | 5.813 |
| Q6_K_P | 6.250 |
| Q8_K_P | 8.133 |

Dung lượng file không phải tổng RAM/VRAM cần dùng.

## Context và đồng thời

llama.cpp ghim `b11981`, continuous batching bật, pool KV tách theo slot. Tham số context tổng = context mỗi lượt × số slot: **128000 / 384000 / 640000** cho **1 / 3 / 5** slot. Context gồm template, hướng dẫn, lịch sử, input và output; input + output phải nằm trong context từng lượt. Trần output 64000 không có nghĩa mọi câu sẽ sinh đủ 64000; EOS vẫn hoạt động.

Notebook đối chiếu `/props` về context mỗi slot, số slot và file; với `n_predict=-1` đặc thù b11981, kiểm tra lệnh tiến trình thật qua `/proc`. Nếu cấu hình thực nhận sai thì không báo sẵn sàng. Không âm thầm chia 128000 cho ba hoặc năm lượt.

Gateway giới hạn đúng số slot đã chọn, thêm tối đa **5 yêu cầu chờ**, mỗi lượt chờ tối đa **60 giây**. Đầy cả hai phần trả HTTP429; hết thời gian chờ chưa gửi tới model cũng trả429. Mỗi lượt đang xử lý có giới hạn tổng30 phút, timeout mạng đọc600 giây. Không retry nội dung đã nhận dở.

Khi ngắt streaming, thao tác đóng kết nối model được bảo vệ khỏi việc hủy của task group và có hạn5giây; slot được giải phóng sau bước dọn này. Đã kiểm thử cả thao tác đóng bất đồng bộ có chờ, không chỉ mock đóng tức thì.

`dispatched` chỉ nghĩa đã chuyển tới llama.cpp; `streaming` nghĩa đã nhận dữ liệu luồng. Số slot có `is_processing=true` tại endpoint xác thực `/v1/runtime` mới là bằng chứng model đang xử lý. Ba xử lý + hai chờ không phải năm sinh đồng thời. Request ID riêng, hủy/disconnect/lỗi/hết lease giải phóng đúng lượt; không lưu prompt hoặc hàng đợi vào database.

Đổi model/context/slot rồi chạy lại sẽ tải file trước, chỉ thay model khi không có lượt đang xử lý hoặc đang chờ. Nếu đang bận thì từ chối đổi rõ ràng và giữ máy cũ. Nếu nạp mới thất bại thì không báo đã áp dụng; có thể chủ động chọn **Khôi phục cấu hình trước** khi lease còn hiệu lực. Nạp lại có thể mất nhiều phút và nhiều GB.

## Giới hạn kiểm chứng và an toàn

Đã có kiểm thử tự động và thử Chromium qua client/gateway thật với inference mô phỏng. **Chưa có benchmark GPU thật của bản này**, chưa chứng minh Q8 +128000 mỗi slot +3/5 vừa T4, chưa thử hết context hoặc sinh đủ64000 token. Chẩn đoán cho xem VRAM hiện dùng/tổng và RAM khả dụng nếu đọc được, không in key hoặc log riêng tư. Lấy mẫu hiện tại không phải đỉnh bộ nhớ benchmark.

Giữ nguyên xác thực, heartbeat, lease và thu hồi. Không cần Colab Secrets, token Google hoặc Cloudflare quản trị. Không gửi key/token vào chat hoặc URL. Notebook mới không tự cập nhật runtime cũ; chỉ chạy phiên mới khi chủ động quyết định. Notebook cá nhân cũ và hostname cá nhân độc lập.

## Quay về

- Tải thấp: chọn **1** slot rồi chủ động chạy lại khi máy rảnh; vẫn giữ Q8/128000/64000.
- Bản trước: [Open in Colab e3c27d5](https://colab.research.google.com/github/Canhettg1133/storyforge-colab/blob/e3c27d5348be0708bab3fb341d5df8e9914ad1ab/StoryForge-Personal-AI.ipynb). Bản đó chỉ có một slot và chưa có danh sách11 lựa chọn.
- Không sửa lịch sử hoặc force-push để rollback; StoryForge đổi URL ghim phiên bản ở backend nếu cần.
