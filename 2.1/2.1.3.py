def duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

nums1 = [1,2,3,4]
nums2 = [1,1,1,3,3,4,3,2,4,2]
nums3 = [1,2,3,1]

print(duplicate(nums1), duplicate(nums2), duplicate(nums3))