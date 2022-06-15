---------------------Total locksmiths jobs for today
SELECT
COUNT(*) AS "Today's total locksmiths jobs"
FROM [dbo].[Policy_LocksmithDetails] LD
LEFT JOIN [dbo].[Lookup_Locksmiths] LS
ON LD.LocksmithID = LS.ID
WHERE LD.Selected = 1
AND LS.LocksmithName LIKE ('WGTK%')
AND CAST(LD.AvailableFromDate AS DATE) = CAST(GETDATE() AS DATE);