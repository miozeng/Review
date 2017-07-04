package com.fwd.eprecious.service.security;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.security.access.ConfigAttribute;
import org.springframework.security.access.SecurityConfig;
import org.springframework.security.web.FilterInvocation;
import org.springframework.security.web.access.intercept.FilterInvocationSecurityMetadataSource;

import com.fwd.eprecious.dao.MenuDao;
import com.fwd.eprecious.dao.RoleDao;
import com.fwd.eprecious.dto.UserDetail;
import com.fwd.eprecious.entity.Menu;
import com.fwd.eprecious.entity.Role;
import com.fwd.eprecious.util.SpringSecuritySeesionUtil;


/**
 * load role and menu 
 * */
public class MySecurityMetadataSource implements FilterInvocationSecurityMetadataSource {
	
	
	private MenuDao menuDao;

	public void setMenuDao(MenuDao menuDao) {
		this.menuDao = menuDao;
	}
	private static Map<String, Collection<ConfigAttribute>> resourceMap = null;

	public Collection<ConfigAttribute> getAllConfigAttributes() {
		return null;
	}

	public boolean supports(Class<?> clazz) {
		return true;
	}
	private void loadResourceDefine() {
		if (resourceMap == null) {
			resourceMap = new HashMap<String, Collection<ConfigAttribute>>();
			List<Menu> menus = menuDao.findAll();
			for (Menu menu : menus) {
				Collection<ConfigAttribute> configAttributes = new ArrayList<ConfigAttribute>();
				for( Role role :menu.getRoles()) {
					ConfigAttribute configAttribute = new SecurityConfig("ROLE_" + role.getRoleName());
					configAttributes.add(configAttribute);
				}
				resourceMap.put(menu.getUrl(), configAttributes);
			}
		}
	}

	public Collection<ConfigAttribute> getAttributes(Object object) throws IllegalArgumentException {
		String requestUrl = ((FilterInvocation) object).getRequestUrl();
		if(resourceMap == null) {
			loadResourceDefine();
		}
		if(requestUrl.indexOf("?")>-1){
			requestUrl=requestUrl.substring(0,requestUrl.indexOf("?"));
		}
		Collection<ConfigAttribute> configAttributes = resourceMap.get(requestUrl);
		if (configAttributes == null) {
			 requestUrl = requestUrl.substring(1,requestUrl.length());
			 requestUrl =requestUrl.substring(0, requestUrl.indexOf("/"));
			 configAttributes = resourceMap.get(requestUrl);
		}
		// if return null MyAccessDecisionManager will not doing
		if (configAttributes == null) {
			Collection<ConfigAttribute> returnCollection = new ArrayList<ConfigAttribute>();
			returnCollection.add(new SecurityConfig("ROLE_NO_USER"));
			return returnCollection;
		}
		return configAttributes;
	}
	


}